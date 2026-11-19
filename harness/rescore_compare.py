"""Compare the round-1 scores (runs/<run_id>/fields.csv) with a re-score (reports/rescore_r1/<run_id>/fields.csv).

  uv run python -m harness.rescore_compare [--new reports/rescore_r1] [--old-check reports/gt_check]
      [--new-check reports/gt_check_rescored] [--out reports/rescore_r1/compare.md]

Every row whose outcome changed is attributed to one cause, in this order:
  excluded     the field was removed from answers.json (invoice total not printed);
  gt_fix       the answer changed (reports/gt_check/applied_fixes.csv);
  accepted     TP through an `accepted` variant; accept_from: TP through the other total field;
  <rule>       the smallest set of normalize.RULES that turns the round-1 comparison into TP (single rules first,
               then pairs).
With --mid (an intermediate re-score, e.g. stage 0 in reports/rescore_r1) the report has three stages per model:
round 1 -> mid -> new, with value accuracy also without documents tagged quality=low, the "format ok" share, L1/L2
of each stage, every row whose outcome changed between mid and new with its cause, and every correct -> wrong
transition (TP/TN -> WV/FN/FF) listed one by one.
Read-only over runs/; writes only --out.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import pandas as pd

from harness import normalize as N
from harness import score as S
from harness.gt_check import decode_pred, model_short

ROOT = Path(__file__).resolve().parents[1]
OUTCOMES = ("TP", "WV", "FN", "TN", "FF")


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def metrics(df: pd.DataFrame) -> dict:
    c = df["outcome"].value_counts()
    tp, wv, fn, tn, ff = (int(c.get(o, 0)) for o in OUTCOMES)
    return {"TP": tp, "WV": wv, "FN": fn, "TN": tn, "FF": ff,
            "value_acc": tp / (tp + wv + fn) if tp + wv + fn else float("nan"),
            "invented": ff / (ff + tn) if ff + tn else float("nan")}


WRONG = ("WV", "FN", "FF")


def metrics_q(df: pd.DataFrame) -> dict:
    """metrics() plus accuracy without quality=low documents and the format-ok share of non-null predictions."""
    m = metrics(df)
    q = df["quality"] if "quality" in df else pd.Series("", index=df.index)
    m["value_acc_noq"] = metrics(df[q != "low"])["value_acc"]
    nn = df[df["outcome"].isin(["TP", "WV", "FF"])]
    m["format_ok"] = nn["canonical"].eq("True").mean() if len(nn) else float("nan")
    nm = nn[nn["field"].isin(N.NAME_FIELDS)]
    m["format_ok_names"] = nm["canonical"].eq("True").mean() if len(nm) else float("nan")
    return m


def step_cause(old: dict, new: dict | None) -> str:
    """Cause of a change between two re-scores (same predictions)."""
    if new is None:
        return "excluded_doc" if old["doc_id"] in step_cause.gone_docs else "excluded_field"
    if old["gt"] != new["gt"]:
        return "gt_fix"
    if new.get("matched_by", "") != old.get("matched_by", ""):
        return "accepted" if new.get("matched_by") == "accepted" else f"matched_by:{new.get('matched_by')}"
    if old["outcome"] == new["outcome"]:
        return "format_flag" if old.get("canonical") != new.get("canonical") else "other"
    return "scorer"


step_cause.gone_docs = set()


def three_stage(a, runs, p) -> list[str]:
    rows, lv, changes, c2w, fmt = [], [], Counter(), [], Counter()
    for rid in runs:
        m = model_short(rid)
        r1 = read(ROOT / "runs" / rid / "fields.csv")
        mid, new = read(p["mid"] / rid / "fields.csv"), read(p["new"] / rid / "fields.csv")
        m0, m1, m2 = metrics_q(r1), metrics_q(mid), metrics_q(new)
        rows.append({"model": m,
                     "acc r1 -> stage0 -> stage1": f"{m0['value_acc']:.4f} -> {m1['value_acc']:.4f} -> "
                                                   f"{m2['value_acc']:.4f}",
                     "acc w/o quality=low (stage1)": round(m2["value_acc_noq"], 4),
                     "invented r1 -> stage0 -> stage1": f"{m0['invented']:.4f} -> {m1['invented']:.4f} -> "
                                                        f"{m2['invented']:.4f}",
                     "format ok r1 -> s0 -> s1": f"{m0['format_ok']:.3f} -> {m1['format_ok']:.3f} -> "
                                                 f"{m2['format_ok']:.3f}",
                     "names format ok s0 -> s1": f"{m1['format_ok_names']:.3f} -> {m2['format_ok_names']:.3f}",
                     "TP/WV/FN/TN/FF stage1": "/".join(str(m2[o]) for o in OUTCOMES)})
        step_cause.gone_docs = set(mid["doc_id"]) - set(new["doc_id"])
        newi = {(r["doc_id"], r["field"]): r for r in new.to_dict("records")}
        for r in mid.to_dict("records"):
            n = newi.get((r["doc_id"], r["field"]))
            if n is not None and n["outcome"] == r["outcome"] and n["gt"] == r["gt"] and \
                    n["canonical"] == r["canonical"] and n.get("matched_by", "") == r.get("matched_by", ""):
                continue
            c = step_cause(r, n)
            t = f"{r['outcome']}->{n['outcome'] if n else '(excluded)'}"
            changes[(c, t)] += 1
            if c == "format_flag":
                fmt[(r["field"], f"{r['canonical']}->{n['canonical']}")] += 1
            if n is not None and r["outcome"] in ("TP", "TN") and n["outcome"] in WRONG:
                c2w.append({"model": m, "doc_id": r["doc_id"], "field": r["field"], "transition": t,
                            "gt stage0": r["gt"], "gt stage1": n["gt"], "pred": r["pred"], "cause": c})
        # round 1 -> stage 1 correct -> wrong (should be only intended GT changes)
        for r in r1.to_dict("records"):
            n = newi.get((r["doc_id"], r["field"]))
            if n is not None and r["outcome"] in ("TP", "TN") and n["outcome"] in WRONG:
                c2w.append({"model": m, "doc_id": r["doc_id"], "field": r["field"],
                            "transition": f"r1 {r['outcome']}->s1 {n['outcome']}", "gt stage0": r["gt"],
                            "gt stage1": n["gt"], "pred": r["pred"], "cause": cause(r, n) + " (r1->s1)"})
    for name, d in (("round 1", p["old_check"]), ("stage 0", p["mid_check"]), ("stage 1", p["new_check"])):
        v = read(d / "votes.csv")
        c = v["level"].value_counts()
        lv.append({"stage": name, "check": str(d.relative_to(ROOT)), "keys": len(v), "L1": int(c.get("L1", 0)),
                   "L2": int(c.get("L2", 0))})
    acc = pd.DataFrame(rows)
    ch = pd.DataFrame([{"cause": c, "transition": t, "rows (6 models)": n}
                       for (c, t), n in sorted(changes.items(), key=lambda kv: (-kv[1], kv[0]))])
    ff = pd.DataFrame([{"field": f, "canonical": t, "rows": n} for (f, t), n in sorted(fmt.items())])
    cw = pd.DataFrame(c2w).drop_duplicates() if c2w else pd.DataFrame()
    return ["# Round 1 re-scored: original r1 -> stage 0 -> stage 1\n",
            "Generated by `uv run python -m harness.rescore_compare --mid ...`. r1 = `runs/<run>/fields.csv` (round-1 "
            f"scorer and answers); stage 0 = `{p['mid'].relative_to(ROOT)}`; stage 1 = `{p['new'].relative_to(ROOT)}` "
            "(same predictions; current answers.json and scorer; models not re-run).\n",
            "Value accuracy = TP / (TP + WV + FN); invented = FF / (FF + TN); format ok = canonical share of non-null "
            "predictions (stage 1: a correct name with extra text is not canonical). The denominators differ between "
            "stages: fields and documents excluded from final/ are not scored.\n",
            "## Per model\n", acc.to_markdown(index=False),
            "\n## Suspect levels (gt_check)\n", pd.DataFrame(lv).to_markdown(index=False),
            "\n## Stage 0 -> stage 1: what moved the rows (all 6 models)\n",
            "excluded_doc / excluded_field: removed from final/ (wild__0426/0428; mask probes); gt_fix: answer changed; "
            "accepted: TP through a new `accepted` value; format_flag: same outcome, canonical changed (1.9a).\n",
            ch.to_markdown(index=False) if len(ch) else "_(none)_",
            "\n### Format flag changes by field\n", ff.to_markdown(index=False) if len(ff) else "_(none)_",
            "\n## Correct -> wrong transitions (TP/TN -> WV/FN/FF), one per row\n",
            cw.to_markdown(index=False) if len(cw) else "_(none)_", ""]


def cause(old: dict, new: dict | None) -> str:
    if new is None:
        return "excluded"
    if old["gt"] != new["gt"]:
        return "gt_fix"
    mb = new.get("matched_by", "")
    if mb == "accepted":
        return "accepted"
    if mb.startswith("from:"):
        return "accept_from"
    gt, pred = old["gt"] or None, decode_pred(old["pred"])
    rules = sorted(N.RULES)
    for k in (1, 2, 3):
        for combo in itertools.combinations(rules, k):
            if S.outcome(old["field"], gt, pred, rules=frozenset(combo)).outcome == new["outcome"]:
                return "+".join(combo)
    return "other"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--runs-from", default="protocol/round1.json")
    ap.add_argument("--new", default="reports/rescore_r1")
    ap.add_argument("--old-check", default="reports/gt_check")
    ap.add_argument("--new-check", default="reports/gt_check_rescored")
    ap.add_argument("--out", default="reports/rescore_r1/compare.md")
    ap.add_argument("--mid", help="intermediate re-score (three-stage report), e.g. reports/rescore_r1")
    ap.add_argument("--mid-check", default="reports/gt_check_rescored")
    a = ap.parse_args(argv)
    p = {k: (Path(v) if Path(v).is_absolute() else ROOT / v) for k, v in vars(a).items() if v is not None}
    runs = [r["run_id"] for r in json.loads(p["runs_from"].read_text())["runs"]]
    if "mid" in p:
        P = three_stage(a, runs, p)
        p["out"].parent.mkdir(parents=True, exist_ok=True)
        p["out"].write_text("\n".join(P) + "\n")
        print("\n".join(P))
        return 0

    rows, causes, trans = [], Counter(), Counter()
    by_model_cause: dict[str, Counter] = {}
    for rid in runs:
        old, new = read(ROOT / "runs" / rid / "fields.csv"), read(p["new"] / rid / "fields.csv")
        mo, mn = metrics(old), metrics(new)
        m = model_short(rid)
        rows.append({"model": m, "acc_old": round(mo["value_acc"], 4), "acc_new": round(mn["value_acc"], 4),
                     "acc_delta_pp": round(100 * (mn["value_acc"] - mo["value_acc"]), 2),
                     "invented_old": round(mo["invented"], 4), "invented_new": round(mn["invented"], 4),
                     **{f"{o}_old": mo[o] for o in OUTCOMES}, **{f"{o}_new": mn[o] for o in OUTCOMES}})
        newi = {(r["doc_id"], r["field"]): r for r in new.to_dict("records")}
        bc = by_model_cause.setdefault(m, Counter())
        for r in old.to_dict("records"):
            n = newi.get((r["doc_id"], r["field"]))
            if n is not None and n["outcome"] == r["outcome"] and n["gt"] == r["gt"]:
                continue
            c = cause(r, n)
            t = f"{r['outcome']}->{n['outcome'] if n else '(excluded)'}"
            causes[c] += 1
            trans[(c, t)] += 1
            bc[c] += 1

    acc = pd.DataFrame(rows)
    lv = []
    for name, d in (("round 1 (old)", p["old_check"]), ("re-scored (new)", p["new_check"])):
        v = read(d / "votes.csv")
        row = {"scoring": name, "keys": len(v)}
        for col, tag in (("level", ""), ("level_raw", " raw")):
            c = v[col].value_counts()
            row[f"L1{tag}"], row[f"L2{tag}"] = int(c.get("L1", 0)), int(c.get("L2", 0))
        lv.append(row)
    lv = pd.DataFrame(lv)

    ct = pd.DataFrame([{"cause": c, "rows": n} for c, n in causes.most_common()])
    tt = pd.DataFrame([{"cause": c, "transition": t, "rows": n} for (c, t), n in
                       sorted(trans.items(), key=lambda kv: (-kv[1], kv[0]))])
    mc = pd.DataFrame(by_model_cause).fillna(0).astype(int)
    mc = mc.loc[ct["cause"]] if len(ct) else mc

    P = ["# Round 1 re-scored: old vs new\n",
         "Generated by `uv run python -m harness.rescore_compare`. Old = `runs/<run>/fields.csv` (round-1 scorer and "
         "answers). New = `reports/rescore_r1/<run>/fields.csv` (`harness.report --out`, same predictions, current "
         "answers.json and scorer; models not re-run). L1/L2 from `reports/gt_check` vs `reports/gt_check_rescored`.\n",
         "Value accuracy = TP / (TP + WV + FN); invented = FF / (FF + TN). The new denominators differ: 60 invoice-total "
         "keys per model (answer null, not masked) are no longer scored.\n",
         "## Per model\n", acc[["model", "acc_old", "acc_new", "acc_delta_pp", "invented_old", "invented_new"]]
         .to_markdown(index=False), "\n", acc[["model"] + [f"{o}_{s}" for o in OUTCOMES for s in ("old", "new")]]
         .to_markdown(index=False),
         "\n## Suspect levels (gt_check)\n",
         "`level`: abstaining (invalid-JSON) models do not vote; `raw`: all 6 models vote.\n", lv.to_markdown(index=False),
         "\n## What moved the rows (all 6 models)\n",
         "One cause per changed row (see the module docstring for the order). Rule names: harness/normalize.py.\n",
         ct.to_markdown(index=False), "\n### Cause x transition\n", tt.to_markdown(index=False),
         "\n### Cause x model\n", mc.to_markdown(), ""]
    p["out"].parent.mkdir(parents=True, exist_ok=True)
    p["out"].write_text("\n".join(P) + "\n")
    print("\n".join(P))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
