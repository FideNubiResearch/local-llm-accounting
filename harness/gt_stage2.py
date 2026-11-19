"""Closeout stage 2 review queue: GT arithmetic, 3-of-6 keys, audit of all-correct keys, hidden controls.

  uv run python -m harness.gt_stage2 [--votes reports/gt_check_rescored_v2/votes.csv]
      [--arith reports/gt_check/stage2/arith.csv] [--verdicts reports/gt_check/review/verdicts.jsonl ...]
      [--out reports/gt_check/stage2]

Streams (queue.csv `stream`; order arith, three_of_six, audit_agree; batches of 25):
  arith         every document with an unexplained GT arithmetic violation (harness/gt_arith.py): one item per
                document, field = the most suspicious involved field (most models wrong; ties by FIELD_PREF);
                fields that already have a verdict are passed over.
  three_of_six  every key with exactly 3 of 6 voting models wrong, unless it already has a verdict.
  audit_agree   AUDIT_N keys where all 6 models are correct (TP or TN), stratified by source (proportional,
                at least AUDIT_MIN per source) and within a source by null / value GT (proportional); seed 0.
  controls      CONTROLS_N keys already judged gt_wrong / ok / model_failure that are L1/L2 in round 1 or in the
                re-score, shuffled in (seed 0) and NOT marked in queue.csv; they take the stream and priority of
                their neighbour. Key: controls_key.csv (expected_value = the earlier reviewer's correct value).
Columns: those of reports/gt_check/review/queue.csv plus `stream`. Creates an empty verdicts.jsonl and a
PROGRESS.md template if missing (never overwrites them). Read-only over runs/ and final/.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

import pandas as pd
import yaml

from harness.gt_check import BATCH, read_verdicts

ROOT = Path(__file__).resolve().parents[1]
MODELS = ("qwen3vl-4b", "qwen3vl-8b", "qwen3.5-4b", "qwen3.5-9b", "gemma4-e4b", "gemma4-12b")
STREAMS = ("arith", "three_of_six", "audit_agree")
PRIORITY = {s: i + 1 for i, s in enumerate(STREAMS)}
AUDIT_N, AUDIT_MIN, CONTROLS_N = 200, 5, 15
CONTROL_VERDICTS = ("gt_wrong", "ok", "model_failure")
CONTROL_MIX = {"gt_wrong": 3, "ok": 3}  # the rest model_failure
FIELD_PREF = ("total_tax", "tax_amount", "total_net", "subtotal", "total_gross", "total", "due_date", "issue_date",
              "period_end", "period_start")
QUEUE_COLUMNS = (["review_id", "priority", "batch", "doc_id", "field", "field_human", "doc_type", "gt", "printed",
                  "consensus_example"] + [f"pred_{m}" for m in MODELS] + ["hint", "page_paths", "stream"])


# ----------------------------------------------------------------------------------------------------------------
# pure helpers (tests/test_gt_stage2.py)
# ----------------------------------------------------------------------------------------------------------------
def allocate(sizes: dict[str, int], n: int, minimum: int = 0) -> dict[str, int]:
    """Proportional allocation of n over strata (largest remainder), each stratum at least min(minimum, size) and
    at most its size. Deterministic (ties by stratum name)."""
    total = sum(sizes.values())
    n = min(n, total)
    alloc = {k: min(minimum, s) for k, s in sizes.items()}
    while True:
        free = {k: s for k, s in sizes.items() if alloc[k] < s}
        rest = n - sum(alloc.values())
        if rest <= 0 or not free:
            return alloc
        # proportional target for the remaining units among strata that can still take more
        base = sum(free.values())
        quota = {k: rest * s / base for k, s in free.items()}
        step = {k: min(int(q), sizes[k] - alloc[k]) for k, q in quota.items()}
        left = rest - sum(step.values())
        for k in sorted(free, key=lambda k: (-(quota[k] - int(quota[k])), k)):
            if left <= 0:
                break
            if alloc[k] + step[k] < sizes[k]:
                step[k] += 1
                left -= 1
        for k, s in step.items():
            alloc[k] += s


def proportional_target(sizes: dict[str, int], n: int, minimum: int) -> dict[str, int]:
    """Proportional allocation where strata whose share is below `minimum` are raised to it and the others share
    the rest proportionally (largest remainder)."""
    n = min(n, sum(sizes.values()))
    fixed: dict[str, int] = {}
    while True:
        rest_keys = [k for k in sizes if k not in fixed]
        rest_n = n - sum(fixed.values())
        base = sum(sizes[k] for k in rest_keys)
        low = [k for k in rest_keys if base and rest_n * sizes[k] / base < min(minimum, sizes[k])]
        if not low:
            break
        for k in low:
            fixed[k] = min(minimum, sizes[k])
    rest_keys = [k for k in sizes if k not in fixed]
    out = dict(fixed)
    out.update(allocate({k: sizes[k] for k in rest_keys}, n - sum(fixed.values())))
    return out


def audit_sample(pool: pd.DataFrame, n: int = AUDIT_N, minimum: int = AUDIT_MIN, seed: int = 0) -> list[str]:
    """Stratified sample of review_ids: by source (proportional, >= minimum), then null / value GT (proportional)."""
    rng = random.Random(seed)
    sizes = pool.groupby("source").size().to_dict()
    target = proportional_target(sizes, n, minimum)
    out = []
    for src in sorted(target):
        g = pool[pool["source"] == src]
        strata = {"null": sorted(g.loc[g["gt"] == "", "review_id"]), "value": sorted(g.loc[g["gt"] != "", "review_id"])}
        sub = allocate({k: len(v) for k, v in strata.items()}, target[src])
        for k in ("null", "value"):
            out += rng.sample(strata[k], sub[k])
    return out


def pick_arith_field(fields: list[str], n_wrong: dict[str, int], reviewed: set[str]) -> str:
    """Most suspicious unreviewed field: most models wrong, ties by FIELD_PREF. '' if all were reviewed."""
    cand = [f for f in fields if f not in reviewed]
    if not cand:
        return ""
    pref = {f: i for i, f in enumerate(FIELD_PREF)}
    return sorted(cand, key=lambda f: (-n_wrong.get(f, 0), pref.get(f, 99), f))[0]


def arith_items(arith: pd.DataFrame, votes: pd.DataFrame, verdicts: dict) -> tuple[list[tuple[str, str]], list[str]]:
    """[(review_id, hint)] for the arith stream, one per document with an unexplained violation; and the documents
    skipped because every involved field already has a verdict."""
    un = arith[arith["status"] == "unexplained"]
    nw = dict(zip(votes["review_id"], votes["n_wrong"].astype(int)))
    items, skipped = [], []
    for doc, g in un.groupby("doc_id", sort=True):
        fields = list(dict.fromkeys(f for fs in g["fields"] for f in fs.split(";")))
        fields = [f for f in fields if f"{doc}::{f}" in nw]
        reviewed = {f for f in fields if f"{doc}::{f}" in verdicts}
        f = pick_arith_field(fields, {f: nw[f"{doc}::{f}"] for f in fields}, reviewed)
        if not f:
            skipped.append(doc)
            continue
        hint = "arith: " + " | ".join(f"{r['check']} {r['values']} diff={r['diff']}" for _, r in g.iterrows())
        items.append((f"{doc}::{f}", hint))
    return items, skipped


def control_pool(votes: pd.DataFrame, r1_levels: dict[str, str], verdicts: dict) -> pd.DataFrame:
    lv = dict(zip(votes["review_id"], votes["level"]))
    rows = []
    for rid, rec in sorted(verdicts.items()):
        if rec.get("verdict") not in CONTROL_VERDICTS or rid not in lv:
            continue
        if lv[rid] in ("L1", "L2") or r1_levels.get(rid) in ("L1", "L2"):
            rows.append({"review_id": rid, "prior_verdict": rec["verdict"],
                         "expected_value": "" if rec.get("correct_value") is None else str(rec["correct_value"]),
                         "prior_batch": rec.get("batch", ""), "level_r1": r1_levels.get(rid, ""),
                         "level_now": lv[rid]})
    return pd.DataFrame(rows, columns=["review_id", "prior_verdict", "expected_value", "prior_batch", "level_r1",
                                       "level_now"])


def pick_controls(pool: pd.DataFrame, n: int = CONTROLS_N, seed: int = 0) -> pd.DataFrame:
    rng = random.Random(seed)
    picked = []
    for v, k in CONTROL_MIX.items():
        ids = sorted(pool.loc[pool["prior_verdict"] == v, "review_id"])
        picked += rng.sample(ids, min(k, len(ids)))
    rest = sorted(set(pool.loc[pool["prior_verdict"] == "model_failure", "review_id"]) - set(picked))
    picked += rng.sample(rest, min(n - len(picked), len(rest)))
    return pool.set_index("review_id").loc[picked].reset_index()


def build(votes: pd.DataFrame, arith: pd.DataFrame, verdicts: dict, field_human: dict[str, str],
          r1_levels: dict[str, str] | None = None, seed: int = 0,
          audit_n: int = AUDIT_N) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """(queue, controls key, info)."""
    order: list[tuple[str, str, str]] = []  # (review_id, stream, hint override)
    seen: set[str] = set()

    def add(rid, stream, hint=""):
        if rid not in seen:
            seen.add(rid)
            order.append((rid, stream, hint))

    a_items, a_skipped = arith_items(arith, votes, verdicts)
    for rid, hint in a_items:
        add(rid, "arith", hint)
    nw, nv = votes["n_wrong"].astype(int), votes["n_voting"].astype(int)
    t36 = votes[(nw == 3) & (nv == 6)].sort_values(["source", "doc_id", "field"])
    n_t36_reviewed = int(t36["review_id"].isin(verdicts).sum())
    for rid in t36["review_id"]:
        if rid not in verdicts:
            add(rid, "three_of_six")

    pool_c = control_pool(votes, r1_levels or {}, verdicts)
    controls = pick_controls(pool_c[~pool_c["review_id"].isin(seen)], seed=seed)
    taken = seen | set(controls["review_id"])
    agree = votes[(votes["n_wrong_raw"].astype(int) == 0) & (nv == 6) & ~votes["review_id"].isin(verdicts)
                  & ~votes["review_id"].isin(taken)]
    for rid in audit_sample(agree, n=audit_n, seed=seed):
        add(rid, "audit_agree")

    crng = random.Random(seed)
    order_c = list(order)
    for rid in controls["review_id"]:
        pos = crng.randint(0, len(order_c))
        nb = order_c[pos - 1] if pos > 0 else order_c[0]
        order_c.insert(pos, (rid, nb[1], ""))

    idx = votes.set_index("review_id")
    rows = []
    for i, (rid, stream, hint) in enumerate(order_c):
        r = idx.loc[rid]
        rows.append({"review_id": rid, "priority": PRIORITY[stream], "batch": i // BATCH + 1, "doc_id": r["doc_id"],
                     "field": r["field"], "field_human": field_human.get(r["field"], r["field"]),
                     "doc_type": r["doc_type"], "gt": r["gt"], "printed": r["printed"],
                     "consensus_example": r["consensus_example"],
                     **{f"pred_{m}": r[f"pred_{m}"] for m in MODELS}, "hint": hint or r["hint"],
                     "page_paths": r["page_paths"], "stream": stream})
    q = pd.DataFrame(rows, columns=QUEUE_COLUMNS)
    bmap = dict(zip(q["review_id"], q["batch"]))
    controls = controls.assign(gt_now=controls["review_id"].map(idx["gt"]),
                               batch=controls["review_id"].map(bmap))
    info = {"arith_skipped_docs": a_skipped, "three_of_six_total": len(t36),
            "three_of_six_reviewed": n_t36_reviewed, "audit_pool": len(agree),
            "streams": q["stream"].value_counts().to_dict(), "n_controls": len(controls),
            "n_batches": int(q["batch"].max()) if len(q) else 0}
    return q, controls, info


PROGRESS_TEMPLATE = """# Stage 2 review progress

Queue: reports/gt_check/stage2/queue.csv ({n} items, {b} batches of {bs}). Verdicts: reports/gt_check/stage2/verdicts.jsonl.
Procedure and verdict vocabulary: reports/gt_check/PLAN.md section 6 (plus `ok` = GT confirmed on the page).

- Batches done: 0 of {b}
- Items reviewed: 0 / {n}
- Last review_id: -
- Verdict counts per stream: arith {{}}, three_of_six {{}}, audit_agree {{}}

## Arithmetic (stream arith)

## 3 of 6 (stream three_of_six)

## Audit of all-correct keys (stream audit_agree)
GT errors found / audited, per source:

## Proposed GT fixes (for the owner)
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--votes", default="reports/gt_check_rescored_v2/votes.csv")
    ap.add_argument("--r1-votes", default="reports/gt_check/votes.csv", help="round-1 levels (control pool)")
    ap.add_argument("--arith", default="reports/gt_check/stage2/arith.csv")
    ap.add_argument("--verdicts", nargs="*", default=["reports/gt_check/review/verdicts.jsonl"])
    ap.add_argument("--out", default="reports/gt_check/stage2")
    a = ap.parse_args(argv)
    P = lambda x: Path(x) if Path(x).is_absolute() else ROOT / x  # noqa: E731
    votes = pd.read_csv(P(a.votes), dtype=str, keep_default_na=False)
    r1 = pd.read_csv(P(a.r1_votes), dtype=str, keep_default_na=False, usecols=["review_id", "level"])
    arith = pd.read_csv(P(a.arith), dtype=str, keep_default_na=False)
    verdicts = {}
    for p in a.verdicts:
        verdicts.update(read_verdicts(P(p))[0])
    fh = yaml.safe_load((ROOT / "protocol" / "fields.yaml").read_text())["fields"]
    q, ctrl, info = build(votes, arith, verdicts, fh, dict(zip(r1["review_id"], r1["level"])))
    out = P(a.out)
    out.mkdir(parents=True, exist_ok=True)
    q.to_csv(out / "queue.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    ctrl.to_csv(out / "controls_key.csv", index=False)
    if not (out / "verdicts.jsonl").exists():
        (out / "verdicts.jsonl").write_text("")
    if not (out / "PROGRESS.md").exists():
        (out / "PROGRESS.md").write_text(PROGRESS_TEMPLATE.format(n=len(q), b=info["n_batches"], bs=BATCH))
    print(json.dumps(info, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
