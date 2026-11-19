"""Score a run against final/ answers.

  uv run python -m harness.report runs/<run_id> [--out DIR]

Writes fields.csv (one row per document x field) and summary.md into runs/<run_id>/, or into --out (re-scoring an
old run with the current answers and scorer without touching runs/), and prints the summary.
Reads only runs/<run_id>/predictions.jsonl and config.json; the models are not re-run.
Outcomes (harness/score.py): TP correct, WV wrong value, FN answered null but a value exists,
TN correct null, FF value invented where the answer is null.
  value accuracy = TP / (TP + WV + FN)     over fields with a value
  invented rate  = FF / (FF + TN)          over fields whose answer is null
  format ok      = share of non-null predictions in the requested form (plain number, ISO date, ...; a correct
                   name found inside extra text is not in the requested form, score.outcome)
Documents tagged `quality: low` in answers.json (manifest column `quality`) stay scored; the summary also gives the
totals without them. Predictions for documents no longer in final/manifest.csv (excluded after the run) are skipped.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import pandas as pd

from harness.score import score_answers

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "final"
GENERATED = {"eurodocbench", "synthetic_receipts", "fatura", "invoice_benchmark", "katanaml_invoices",
             "bank_statement_intel"}   # 00-plan.md section 3.1


def field_rows(run: Path) -> pd.DataFrame:
    man = {r["doc_id"]: r for r in csv.DictReader(open(FINAL / "manifest.csv"))}
    out = []
    for line in (run / "predictions.jsonl").read_text().splitlines():
        p = json.loads(line)
        if p["doc_id"] not in man:          # document excluded from final/ after the run (final/excluded.csv)
            continue
        m = man[p["doc_id"]]
        ans = json.loads((FINAL / "docs" / p["doc_id"] / "answers.json").read_text())
        ds = score_answers(ans, p["parsed"])
        for r in ds.fields:
            out.append({"doc_id": p["doc_id"], "source": m["source"], "kind": "generated" if m["source"] in GENERATED
                        else "real", "lang": m["lang"], "doc_type": m["doc_type"], "variant": m["variant"],
                        "template": m.get("template", ""), "masked": bool(m["masked_field"]),
                        "quality": ans.get("quality", "") or "", "field": r.field,
                        "outcome": r.outcome, "matched_by": r.matched_by, "canonical": r.canonical, "gt": r.gt,
                        "pred": json.dumps(r.pred, ensure_ascii=False) if r.pred is not None else None,
                        "json_valid": ds.json_valid, "strict_json": p["strict_json"], "wall_s": p["wall_s"],
                        "peak_gb": p["peak_gb"], "error": p["error"]})
    return pd.DataFrame(out)


def summarize(df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    def agg(g):
        o = g["outcome"].value_counts()
        tp, wv, fn, tn, ff = (int(o.get(k, 0)) for k in ("TP", "WV", "FN", "TN", "FF"))
        nonnull = g[g["outcome"].isin(["TP", "WV", "FF"])]
        docs = g.drop_duplicates("doc_id")
        return pd.Series({
            "docs": len(docs), "values": tp + wv + fn,
            "value_acc": round(tp / (tp + wv + fn), 3) if tp + wv + fn else None,
            "wrong": wv, "missed": fn, "nulls": tn + ff,
            "invented": round(ff / (tn + ff), 3) if tn + ff else None,
            "format_ok": round(nonnull["canonical"].mean(), 3) if len(nonnull) else None,
            "json_valid": round(docs["json_valid"].mean(), 3),
            "sec_median": round(docs["wall_s"].median(), 1)})
    return df.groupby(by, dropna=False).apply(agg, include_groups=False).reset_index()


def main(run_dir: str, out: str | None = None):
    run = Path(run_dir)
    dest = Path(out) if out else run
    dest.mkdir(parents=True, exist_ok=True)
    df = field_rows(run)
    df.to_csv(dest / "fields.csv", index=False)
    cfg = json.loads((run / "config.json").read_text())
    parts = [f"# {cfg['run_id']}\n", "```", json.dumps(cfg, indent=1), "```\n"]
    if dest != run:
        parts.insert(1, f"Re-scored from `{run}/predictions.jsonl` with the current final/ answers and scorer.\n")
    low = df["quality"].eq("low")
    for title, d, by in [("All", df, ["doc_type"]),
                         ("All without quality=low documents", df[~low], ["doc_type"]),
                         ("Language x type x real/generated", df, ["lang", "doc_type", "kind"]),
                         ("Field", df, ["doc_type", "field"])]:
        parts += [f"## {title}\n"]
        if d is not df:
            parts += [f"{int(low.groupby(df['doc_id']).any().sum())} documents tagged quality=low "
                      f"({int(low.sum())} rows) are left out of this table only.\n"]
        parts += [summarize(d, by).to_markdown(index=False), ""]
    text = "\n".join(parts)
    (dest / "summary.md").write_text(text)
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Score a run against final/ answers.")
    ap.add_argument("run_dir")
    ap.add_argument("--out", help="output directory (default: the run directory)")
    a = ap.parse_args()
    main(a.run_dir, a.out)
