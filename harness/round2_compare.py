"""Round 2: every mode of a finalist against its own base (r1b, P1b, 4 bit) on the same 400 documents.

  uv run python -m harness.round2_compare [--base reports/rescore_r1b] [--new reports/rescore_r2]
      [--protocol protocol/round2.json] [--base-protocol protocol/round1b.json] [--out reports/round2]

Rules: protocol/preregistration.md sections 4-5 (fixed 2026-11-15, before the first round-2 run).
- Metrics as harness/prompt_compare.py: main fields = all but payment_method; primary F1; invented FF/(FF+TN), also
  without receipt subtotal; docs_ok; JSON valid; seconds per document (median); peak memory.
- Paired per (model, mode) on the same (doc_id, field) keys, main fields: better = wrong in base and right in mode,
  worse = the reverse; exact sign test; Holm over all comparisons of round 2, alpha 0.05.
  Verdict: better / worse when the net has that sign and Holm p < 0.05, else "no difference".
- Invented values separately, same paired test over keys whose answer is null (TN <-> FF), own Holm family.
- Best configuration: highest F1 among (model, mode) not worse than its base (the base itself included); F1 within
  0.3 points of the best -> fewer invented, then faster.
- Swap growth during each run from runs/system.jsonl (run window = finished_at minus load_s and the summed
  per-document wall time .. finished_at).
Read-only over its inputs; writes only --out.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from harness.prompt_compare import RIGHT, SEPARATE, fmt, side_row, sign_test

ROOT = Path(__file__).resolve().parents[1]
ALPHA, F1_TIE = 0.05, 0.003


def holm(p: list[float]) -> list[float]:
    """Holm step-down adjusted p-values (monotone, capped at 1)."""
    order = sorted(range(len(p)), key=lambda i: p[i])
    adj, run = [0.0] * len(p), 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (len(p) - rank) * p[i]))
        adj[i] = run
    return adj


def read(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["wall_s"] = df["wall_s"].astype(float)
    df["peak_gb"] = df["peak_gb"].astype(float)
    return df


def paired(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    ka, kb = set(zip(a["doc_id"], a["field"])), set(zip(b["doc_id"], b["field"]))
    if ka != kb:
        raise SystemExit(f"keys differ ({len(ka - kb)} only base, {len(kb - ka)} only mode)")
    j = a.merge(b, on=["doc_id", "field"], suffixes=("_a", "_b"))
    j = j[~j["field"].isin(SEPARATE)]
    ra, rb = j["outcome_a"].isin(RIGHT), j["outcome_b"].isin(RIGHT)
    better, worse = int((~ra & rb).sum()), int((ra & ~rb).sum())
    nul = j[j["outcome_a"].isin(["TN", "FF"])]
    inv_fixed = int(((nul["outcome_a"] == "FF") & (nul["outcome_b"] == "TN")).sum())
    inv_new = int(((nul["outcome_a"] == "TN") & (nul["outcome_b"] == "FF")).sum())
    return {"better": better, "worse": worse, "net": better - worse, "p": sign_test(better, worse),
            "inv_fixed": inv_fixed, "inv_new": inv_new, "p_inv": sign_test(inv_fixed, inv_new)}


def swap_growth(system: Path, windows: dict[str, tuple[str, str]]) -> dict[str, float]:
    if not system.exists():
        return {}
    s = pd.read_json(system, lines=True)
    s["t"] = s["t"].astype(str)
    out = {}
    for rid, (t0, t1) in windows.items():
        w = s[(s["t"] >= t0) & (s["t"] <= t1)]
        out[rid] = float(w["swap_gb"].max() - w["swap_gb"].iloc[0]) if len(w) else float("nan")
    return out


def compare(base: dict[str, pd.DataFrame], modes: list[tuple[str, str, str, pd.DataFrame]],
            swap: dict[str, float] | None = None) -> dict:
    swap = swap or {}
    rows, tests = [], []
    for m, b in sorted(base.items()):
        rows.append({"model": m, "mode": "base", "run_id": "", **side_row(b), "swap_gb": float("nan")})
    for rid, m, mode, d in modes:
        rows.append({"model": m, "mode": mode, "run_id": rid, **side_row(d), "swap_gb": swap.get(rid, float("nan"))})
        tests.append({"model": m, "mode": mode, **paired(base[m], d)})
    t = pd.DataFrame(tests)
    t["p_holm"] = holm(t["p"].tolist())
    t["p_inv_holm"] = holm(t["p_inv"].tolist())
    t["verdict"] = [("better" if n > 0 else "worse") if ph < ALPHA and n != 0 else "no difference"
                    for n, ph in zip(t["net"], t["p_holm"])]
    t["verdict_inv"] = [("fewer" if f > n else "more") if ph < ALPHA and f != n else "no difference"
                        for f, n, ph in zip(t["inv_fixed"], t["inv_new"], t["p_inv_holm"])]
    r = pd.DataFrame(rows).merge(t[["model", "mode", "verdict", "verdict_inv"]], on=["model", "mode"], how="left")
    r["verdict"] = r["verdict"].fillna("base")
    r["verdict_inv"] = r["verdict_inv"].fillna("base")
    return {"rows": r, "tests": t, "best": best(r)}


def best(rows: pd.DataFrame) -> pd.DataFrame:
    c = rows[rows["verdict"] != "worse"].copy()
    top = c["f1"].max()
    c["within_tie"] = c["f1"] >= top - F1_TIE
    c = c.sort_values(["within_tie", "invented", "sec_median", "f1"], ascending=[False, True, True, False])
    c = pd.concat([c[c["within_tie"]], c[~c["within_tie"]].sort_values("f1", ascending=False)])
    c["rank"] = range(1, len(c) + 1)
    return c.reset_index(drop=True)


def report(res: dict, out: Path, n_docs: int) -> str:
    rows, t, b = res["rows"], res["tests"], res["best"]
    pct = ["f1", "precision", "value_acc", "invented", "invented_no_subtotal", "docs_ok", "json_valid",
           "payment_acc"]
    cols = ["model", "mode", "f1", "precision", "value_acc", "invented", "invented_no_subtotal", "docs_ok",
            "json_valid", "payment_acc", "sec_median", "peak_gb", "swap_gb", "verdict", "verdict_inv"]
    tp = t.copy()
    for c in ("p", "p_holm", "p_inv", "p_inv_holm"):
        tp[c] = tp[c].map(lambda p: "<0.0001" if p < 1e-4 else f"{p:.4f}")
    parts = [
        "# Round 2: modes vs base (r1b, P1b, 4 bit)\n",
        f"Same {n_docs} documents (protocol/samples/round2.txt) and keys on both sides, current scorer. Rules: "
        "protocol/preregistration.md sections 4-5. Generated by `harness/round2_compare.py`.\n",
        "Main score: all fields except payment_method. Percentages; sec_median per document; peak_gb from the "
        "run; swap_gb = swap growth during the run (runs/system.jsonl).\n",
        "## Per model and mode\n",
        fmt(rows[cols], pct, {"sec_median": 1, "peak_gb": 2, "swap_gb": 2}), "",
        "## Paired tests vs base (main fields; Holm over all comparisons)\n",
        "better = wrong in base, right in mode; worse = the reverse. inv_fixed = FF in base -> TN in mode; "
        "inv_new = TN -> FF (own Holm family).\n",
        fmt(tp[["model", "mode", "better", "worse", "net", "p", "p_holm", "verdict", "inv_fixed", "inv_new",
                "p_inv", "p_inv_holm", "verdict_inv"]], []), "",
        "## Best configuration\n",
        f"Highest F1 among configurations not worse than their base; within {F1_TIE * 100:.1f} points of the best "
        "-> fewer invented, then faster.\n",
        fmt(b[["rank", "model", "mode", "f1", "invented", "sec_median", "peak_gb", "verdict", "within_tie"]],
            ["f1", "invented"], {"sec_median": 1, "peak_gb": 2}), "",
    ]
    out.mkdir(parents=True, exist_ok=True)
    rows.to_csv(out / "models.csv", index=False)
    t.to_csv(out / "tests.csv", index=False)
    b.to_csv(out / "best.csv", index=False)
    text = "\n".join(parts)
    (out / "compare.md").write_text(text)
    return text


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", default="reports/rescore_r1b")
    ap.add_argument("--new", default="reports/rescore_r2")
    ap.add_argument("--protocol", default="protocol/round2.json")
    ap.add_argument("--base-protocol", default="protocol/round1b.json")
    ap.add_argument("--system", default="runs/system.jsonl")
    ap.add_argument("--out", default="reports/round2")
    a = ap.parse_args(argv)
    p = lambda x: Path(x) if Path(x).is_absolute() else ROOT / x  # noqa: E731
    proto = json.loads(p(a.protocol).read_text())
    docs = set(p(proto["docs"]).read_text().split())
    finalists = {r["run_id"].split("__")[1] for r in proto["runs"]}
    base = {}
    for r in json.loads(p(a.base_protocol).read_text())["runs"]:
        m = r["run_id"].split("__")[1]
        if m in finalists:
            df = read(p(a.base) / r["run_id"] / "fields.csv")
            base[m] = df[df["doc_id"].isin(docs)].reset_index(drop=True)
    modes, windows = [], {}
    for r in proto["runs"]:
        rid = r["run_id"]
        d = read(p(a.new) / rid / "fields.csv")
        modes.append((rid, rid.split("__")[1], rid.split("__")[2], d))
        cfg = json.loads((ROOT / "runs" / rid / "config.json").read_text())
        if cfg.get("finished_at"):
            fin = pd.Timestamp(cfg["finished_at"])
            dur = d.drop_duplicates("doc_id")["wall_s"].sum() + float(cfg.get("load_s") or 0)
            windows[rid] = (str(fin - pd.Timedelta(seconds=dur)), str(fin))
    res = compare(base, modes, swap_growth(p(a.system), windows))
    print(report(res, p(a.out), len(docs)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
