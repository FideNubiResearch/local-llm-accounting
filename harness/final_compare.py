"""Final run (protocol/round_final.json): gemma4-12b q6 vs qwen3.5-4b q6 on the whole final/ set.

  uv run python -m harness.final_compare [--out reports/final]

Metrics are those of harness/prompt_compare.py (main fields = all but payment_method). Parts:
  1. both configurations and their own 4-bit bases (r1b, P1b) on all documents;
  2. paired: gemma q6 vs qwen3.5-4b q6, and each q6 vs its 4-bit base, on the same (doc_id, field) keys
     (better = wrong in the first and right in the second, exact sign test; descriptive, not a pre-registered family);
  3. split real / generated documents (the manifest column `kind`);
  4. by language inside each kind, with Wilson 95 % intervals. Exploratory: language is confounded with source
     and type (it/es/nl/pl are generated only), small groups are marked.
Read-only over its inputs; writes only --out.
"""
from __future__ import annotations

import argparse
from math import sqrt
from pathlib import Path

import pandas as pd

from harness.prompt_compare import RIGHT, SEPARATE, sign_test, side_row, metrics

ROOT = Path(__file__).resolve().parents[1]
MIN_VALUES = 150          # fewer values than this: shown, not interpreted


def read(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["wall_s"] = df["wall_s"].astype(float)
    df["peak_gb"] = df["peak_gb"].astype(float)
    return df


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def paired(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """a vs b on the same main-field keys: better = wrong in a, right in b."""
    k = ["doc_id", "field"]
    a = a[~a["field"].isin(SEPARATE)].set_index(k)["outcome"]
    b = b[~b["field"].isin(SEPARATE)].set_index(k)["outcome"]
    if set(a.index) != set(b.index):
        raise SystemExit(f"keys differ: {len(set(a.index) ^ set(b.index))} not shared")
    ra, rb = a.isin(RIGHT), b.reindex(a.index).isin(RIGHT)
    better, worse = int((~ra & rb).sum()), int((ra & ~rb).sum())
    return {"better": better, "worse": worse, "net": better - worse, "p": sign_test(better, worse), "keys": len(a)}


def pct(x: float, d: int = 1) -> str:
    return "—" if x != x else f"{100 * x:.{d}f}"


def table(rows: list[dict], cols: list[tuple[str, str]]) -> str:
    out = ["| " + " | ".join(h for h, _ in cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    out += ["| " + " | ".join(str(r[k]) for _, k in cols) + " |" for r in rows]
    return "\n".join(out)


def by_group(df: pd.DataFrame, keys: list[str]) -> list[dict]:
    main = df[~df["field"].isin(SEPARATE)]
    rows = []
    for g, d in main.groupby(keys):
        g = g if isinstance(g, tuple) else (g,)
        m = metrics(d)
        vals = d["outcome"].isin(["TP", "WV", "FN"])
        tp = int((d["outcome"] == "TP").sum())
        lo, hi = wilson(tp, int(vals.sum()))
        rows.append({**dict(zip(keys, g)), "docs": d["doc_id"].nunique(), "values": int(vals.sum()),
                     "acc": pct(m["value_acc"]), "ci": f"{pct(lo)}–{pct(hi)}", "f1": pct(m["f1"]),
                     "inv": pct(m["invented"]), "note": "few" if vals.sum() < MIN_VALUES else ""})
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", default="reports/rescore_final")
    ap.add_argument("--base", default="reports/rescore_r1b")
    ap.add_argument("--out", default="reports/final")
    a = ap.parse_args(argv)
    fin, base = ROOT / a.final, ROOT / a.base
    cfg = {
        "gemma4-12b q6": read(fin / "f__gemma4-12b__q6" / "fields.csv"),
        "qwen3.5-4b q6": read(fin / "f__qwen3.5-4b__q6" / "fields.csv"),
    }
    bases = {
        "gemma4-12b q6": read(base / "r1b__gemma4-12b__P1b" / "fields.csv"),
        "qwen3.5-4b q6": read(base / "r1b__qwen3.5-4b__P1b" / "fields.csv"),
    }
    n_docs = {k: v["doc_id"].nunique() for k, v in cfg.items()}
    L = ["# Final run: gemma4-12b q6 vs qwen3.5-4b q6", "",
         f"Documents: {n_docs}. Metrics as in harness/prompt_compare.py (main fields, payment_method excluded). "
         "Paired comparisons and breakdowns are descriptive, not part of the pre-registered family of tests.", ""]

    # 1. overall
    rows = []
    for name in cfg:
        for tag, df in ((f"{name}", cfg[name]), (f"{name.split()[0]} 4-bit (r1b base)", bases[name])):
            r = side_row(df)
            rows.append({"cfg": tag, "docs": df["doc_id"].nunique(), "f1": pct(r["f1"]), "acc": pct(r["value_acc"]),
                         "inv": pct(r["invented"]), "docs_ok": pct(r["docs_ok"]), "json": pct(r["json_valid"]),
                         "sec": f"{r['sec_median']:.1f}", "hours": f"{r['hours']:.1f}", "peak": f"{r['peak_gb']:.1f}"})
    L += ["## 1. All documents", "", table(rows, [("Configuration", "cfg"), ("Docs", "docs"), ("F1, %", "f1"),
          ("Correct values, %", "acc"), ("Invented, %", "inv"), ("Error-free docs, %", "docs_ok"),
          ("JSON, %", "json"), ("s/doc", "sec"), ("Hours", "hours"), ("Peak, GB", "peak")]), ""]

    # 2. paired
    pr = []
    p = paired(cfg["qwen3.5-4b q6"], cfg["gemma4-12b q6"])
    pr.append({"cmp": "gemma q6 vs qwen3.5-4b q6", **p})
    for name in cfg:
        p = paired(bases[name], cfg[name])
        pr.append({"cmp": f"{name} vs its own 4-bit base", **p})
    for r in pr:
        r["p"] = f"{r['p']:.3g}"
    L += ["## 2. Paired comparison (doc x field keys, main fields)", "",
          "Better = wrong in the configuration left of \"vs\" and right in the other one.", "",
          table(pr, [("Comparison", "cmp"), ("Keys", "keys"), ("Better", "better"), ("Worse", "worse"),
                     ("Net", "net"), ("p (exact sign test)", "p")]), ""]

    # 3. real / generated
    L += ["## 3. Real and generated documents", ""]
    for name, df in cfg.items():
        L += [f"**{name}**", "", table(by_group(df, ["kind"]), [("Kind", "kind"), ("Docs", "docs"), ("Values", "values"),
              ("Correct, %", "acc"), ("95 % interval", "ci"), ("F1, %", "f1"), ("Invented, %", "inv")]), ""]
    for name, df in bases.items():
        L += [f"**{name.split()[0]} 4-bit (base)**", "", table(by_group(df, ["kind"]), [("Kind", "kind"),
              ("Docs", "docs"), ("Values", "values"), ("Correct, %", "acc"), ("95 % interval", "ci"),
              ("F1, %", "f1"), ("Invented, %", "inv")]), ""]

    # 4. language within kind
    L += ["## 4. By language within document kind (exploratory)", "",
          "Language is confounded with source and type: it/es/nl/pl are generated only. Groups with fewer than "
          f"{MIN_VALUES} values are marked \"few\" and not interpreted. Languages are only comparable within "
          "one kind.", ""]
    for name, df in cfg.items():
        rows = by_group(df, ["kind", "lang"])
        L += [f"**{name}**", "", table(rows, [("Kind", "kind"), ("Language", "lang"), ("Docs", "docs"),
              ("Values", "values"), ("Correct, %", "acc"), ("95 % interval", "ci"), ("F1, %", "f1"),
              ("Invented, %", "inv"), ("", "note")]), ""]

    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "compare.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
