"""Compare two rounds that differ only in the prompt (r1 = P1, r1b = P1b), model by model, on the same keys.

  uv run python -m harness.prompt_compare [--old reports/rescore_r1_v4] [--new reports/rescore_r1b]
      [--old-protocol protocol/round1.json] [--new-protocol protocol/round1b.json] [--out reports/r1_vs_r1b]

Both sides must be scored by the current scorer (re-scores via harness.report --out), so the only difference is the
prompt. Every model must have the same (doc_id, field) keys on both sides; the check fails otherwise.

Main score = all fields except SEPARATE (payment_method, shown on its own row: a category, not a value read from
the page; owner 2026-11-15). Per model and side:
  value_acc  = TP / (TP + WV + FN)            fields with a value
  invented   = FF / (FF + TN)                 fields whose answer is null; also without receipt subtotal
  precision  = TP / (TP + WV + FF)            non-null answers that are right
  recall     = TP / (TP + WV + FN)            (= value_acc)
  F1         = harmonic mean of precision and recall
  docs_ok    = documents with every main field right (TP or TN)
  json_valid = documents whose output parsed; hours = sum of per-document wall time (model load excluded)
Paired change per model: keys right on P1 and wrong on P1b and the reverse, with an exact two-sided sign
(McNemar) p-value.
Finalists (00-plan.md section 8.1, example rule, not pre-registered): the 3 best models on the new side by main F1
among those with json_valid >= 0.90; a tie (F1 equal to 3 decimals) goes to the lower invented rate.
Read-only over its inputs; writes only --out.
"""
from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEPARATE = {"payment_method"}
RIGHT = {"TP", "TN"}
N_FINALISTS, MIN_JSON = 3, 0.90


def model_short(run_id: str) -> str:
    return run_id.split("__")[1]


def metrics(g: pd.DataFrame) -> dict:
    o = g["outcome"].value_counts()
    tp, wv, fn, tn, ff = (int(o.get(k, 0)) for k in ("TP", "WV", "FN", "TN", "FF"))
    prec = tp / (tp + wv + ff) if tp + wv + ff else float("nan")
    rec = tp / (tp + wv + fn) if tp + wv + fn else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else float("nan")
    ns = g[~((g["doc_type"] == "receipt") & (g["field"] == "subtotal"))]["outcome"].value_counts()
    ff2, tn2 = int(ns.get("FF", 0)), int(ns.get("TN", 0))
    return {"value_acc": rec, "precision": prec, "f1": f1,
            "invented": ff / (ff + tn) if ff + tn else float("nan"),
            "invented_no_subtotal": ff2 / (ff2 + tn2) if ff2 + tn2 else float("nan"),
            "FF": ff, "TN": tn, "n": len(g)}


def sign_test(b: int, c: int) -> float:
    """Exact two-sided McNemar / sign test on the discordant pairs b, c."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def load(root: Path, protocol: Path) -> dict[str, pd.DataFrame]:
    runs = json.loads(protocol.read_text())["runs"]
    out = {}
    for r in runs:
        df = pd.read_csv(root / r["run_id"] / "fields.csv", dtype=str, keep_default_na=False)
        df["wall_s"] = df["wall_s"].astype(float)
        df["peak_gb"] = df["peak_gb"].astype(float)
        out[model_short(r["run_id"])] = df
    return out


def side_row(df: pd.DataFrame) -> dict:
    main = df[~df["field"].isin(SEPARATE)]
    m = metrics(main)
    docs = df.drop_duplicates("doc_id")
    ok = main.assign(r=main["outcome"].isin(RIGHT)).groupby("doc_id")["r"].all()
    sep = df[df["field"].isin(SEPARATE)]
    return {**m, "docs_ok": ok.mean(), "json_valid": (docs["json_valid"] == "True").mean(),
            "hours": docs["wall_s"].sum() / 3600, "sec_median": docs["wall_s"].median(),
            "peak_gb": docs["peak_gb"].max(),
            "payment_acc": metrics(sep)["value_acc"] if len(sep) else float("nan")}


def compare(old: dict[str, pd.DataFrame], new: dict[str, pd.DataFrame]) -> dict:
    if set(old) != set(new):
        raise SystemExit(f"models differ: {sorted(old)} vs {sorted(new)}")
    rows, fields, paired, groups = [], [], [], []
    for m in sorted(new):
        a, b = old[m], new[m]
        ka, kb = set(zip(a["doc_id"], a["field"])), set(zip(b["doc_id"], b["field"]))
        if ka != kb:
            raise SystemExit(f"{m}: keys differ ({len(ka - kb)} only old, {len(kb - ka)} only new)")
        for side, d in (("P1", a), ("P1b", b)):
            rows.append({"model": m, "prompt": side, **side_row(d)})
        j = a.merge(b, on=["doc_id", "field"], suffixes=("_a", "_b"))
        jm = j[~j["field"].isin(SEPARATE)]
        ra, rb = jm["outcome_a"].isin(RIGHT), jm["outcome_b"].isin(RIGHT)
        worse, better = int((ra & ~rb).sum()), int((~ra & rb).sum())
        paired.append({"model": m, "better": better, "worse": worse, "net": better - worse,
                       "p_sign": sign_test(better, worse)})
        for (dt, f), g in j.groupby(["doc_type_a", "field"]):
            ma = metrics(g.rename(columns={"outcome_a": "outcome", "doc_type_a": "doc_type"}))
            mb = metrics(g.rename(columns={"outcome_b": "outcome", "doc_type_a": "doc_type"}))
            fields.append({"model": m, "doc_type": dt, "field": f, "values": int(g["outcome_a"].isin(
                ["TP", "WV", "FN"]).sum()), "acc_P1": ma["value_acc"], "acc_P1b": mb["value_acc"],
                "FF_P1": ma["FF"], "FF_P1b": mb["FF"]})
        for key in ("doc_type_a", "kind_a"):
            for k, g in jm.groupby(key):
                ma = metrics(g.rename(columns={"outcome_a": "outcome", "doc_type_a": "doc_type"}))
                mb = metrics(g.rename(columns={"outcome_b": "outcome", "doc_type_a": "doc_type"}))
                groups.append({"model": m, "group": f"{key[:-2]}={k}", "f1_P1": ma["f1"], "f1_P1b": mb["f1"],
                               "inv_P1": ma["invented"], "inv_P1b": mb["invented"]})
    return {"rows": pd.DataFrame(rows), "fields": pd.DataFrame(fields), "paired": pd.DataFrame(paired),
            "groups": pd.DataFrame(groups)}


def finalists(rows: pd.DataFrame, side: str = "P1b") -> pd.DataFrame:
    r = rows[rows["prompt"] == side].copy()
    r["eligible"] = r["json_valid"] >= MIN_JSON
    r["f1_r"] = r["f1"].round(3)
    r = r.sort_values(["eligible", "f1_r", "invented"], ascending=[False, False, True]).reset_index(drop=True)
    r["rank"] = range(1, len(r) + 1)
    r["finalist"] = r["eligible"] & (r["rank"] <= N_FINALISTS)
    return r


def fmt(df: pd.DataFrame, pct: list[str], dec: dict[str, int] | None = None) -> str:
    d = df.copy()
    for c in pct:
        d[c] = (d[c] * 100).map(lambda x: "" if pd.isna(x) else f"{x:.1f}")
    for c, n in (dec or {}).items():
        d[c] = d[c].map(lambda x: "" if pd.isna(x) else f"{x:.{n}f}")
    return d.to_markdown(index=False)


def report(res: dict, out: Path) -> str:
    rows, fields, paired, groups = res["rows"], res["fields"], res["paired"], res["groups"]
    fin = finalists(rows)
    w = rows.pivot(index="model", columns="prompt")
    delta = pd.DataFrame({
        "F1 P1": w[("f1", "P1")], "F1 P1b": w[("f1", "P1b")],
        "acc P1": w[("value_acc", "P1")], "acc P1b": w[("value_acc", "P1b")],
        "inv P1": w[("invented", "P1")], "inv P1b": w[("invented", "P1b")],
        "inv w/o subtotal P1": w[("invented_no_subtotal", "P1")],
        "inv w/o subtotal P1b": w[("invented_no_subtotal", "P1b")],
        "payment P1": w[("payment_acc", "P1")], "payment P1b": w[("payment_acc", "P1b")]}).reset_index()
    fch = fields.assign(d=fields["acc_P1b"] - fields["acc_P1"])
    big = fch[(fch["values"] >= 30) & (fch["d"].abs() >= 0.03)].sort_values("d")
    ffch = fields.assign(dff=fields["FF_P1b"] - fields["FF_P1"])
    ffbig = ffch[ffch["dff"].abs() >= 10].sort_values("dff")
    parts = [
        "# r1 (P1) vs r1b (P1b)\n",
        "Same 1572 documents and keys, same models and settings, current scorer on both sides "
        "(r1: reports/rescore_r1_v4, r1b: reports/rescore_r1b). Generated by `harness/prompt_compare.py`.\n",
        "Main score: all fields except payment_method (own column). Percentages.\n",
        "## Per model\n",
        fmt(delta, [c for c in delta.columns if c != "model"]), "",
        "## Paired change P1 -> P1b (main fields)\n",
        "better = wrong on P1, right on P1b; worse = the reverse; p = exact sign test.\n",
        fmt(paired.assign(p_sign=paired["p_sign"].map(lambda p: "<0.0001" if p < 1e-4 else f"{p:.4f}")), []), "",
        "## P1b: ranking and finalists\n",
        f"Rule (00-plan.md 8.1, example, not pre-registered): top {N_FINALISTS} by main F1 with JSON valid >= "
        f"{MIN_JSON:.0%}; tie on F1 (3 decimals) -> lower invented.\n",
        fmt(fin[["rank", "model", "f1", "precision", "value_acc", "invented", "invented_no_subtotal", "docs_ok",
                 "json_valid", "payment_acc", "sec_median", "hours", "peak_gb", "finalist"]],
            ["f1", "precision", "value_acc", "invented", "invented_no_subtotal", "docs_ok", "json_valid",
             "payment_acc"], {"sec_median": 1, "hours": 1, "peak_gb": 2}), "",
        "## By document type and real/generated (main fields, F1 and invented)\n",
        fmt(groups, ["f1_P1", "f1_P1b", "inv_P1", "inv_P1b"]), "",
        "## Fields whose accuracy moved by >= 3 points (>= 30 values)\n",
        fmt(big.drop(columns="d"), ["acc_P1", "acc_P1b"]), "",
        "## Fields whose invented count moved by >= 10\n",
        fmt(ffbig.drop(columns="dff"), ["acc_P1", "acc_P1b"]), "",
    ]
    out.mkdir(parents=True, exist_ok=True)
    rows.to_csv(out / "models.csv", index=False)
    fields.to_csv(out / "fields.csv", index=False)
    paired.to_csv(out / "paired.csv", index=False)
    groups.to_csv(out / "groups.csv", index=False)
    fin.to_csv(out / "ranking_P1b.csv", index=False)
    text = "\n".join(parts)
    (out / "compare.md").write_text(text)
    return text


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--old", default="reports/rescore_r1_v4")
    ap.add_argument("--new", default="reports/rescore_r1b")
    ap.add_argument("--old-protocol", default="protocol/round1.json")
    ap.add_argument("--new-protocol", default="protocol/round1b.json")
    ap.add_argument("--out", default="reports/r1_vs_r1b")
    a = ap.parse_args(argv)
    p = lambda x: Path(x) if Path(x).is_absolute() else ROOT / x  # noqa: E731
    res = compare(load(p(a.old), p(a.old_protocol)), load(p(a.new), p(a.new_protocol)))
    print(report(res, p(a.out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
