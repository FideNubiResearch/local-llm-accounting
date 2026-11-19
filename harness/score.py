"""Per-field scoring of one prediction against one ground truth.

Outcome per scalar field:
  TP  gt present, pred correct
  WV  gt present, pred non-null but wrong        (wrong value)
  FN  gt present, pred null / missing             (over-abstention)
  TN  gt null,    pred null / missing             (correct abstention)
  FF  gt null,    pred non-null                   (false fill = hallucination)

Missing keys count as null (ExtractBench convention).
answers.json may give, per field (final/README.md):
  accepted     extra correct values (e.g. brand and legal entity of the seller); the prediction is correct if it
               equals the answer or any of them;
  accept_from  other fields whose prediction also counts for this one (an invoice that prints only one of
               total_gross / total_net: the amount is correct in either field).
Line items are matched with the Hungarian algorithm on row similarity; cells then scored the same way.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linear_sum_assignment

from harness import normalize as N

LIST_FIELDS = {"line_items", "transactions"}


@dataclass
class FieldResult:
    field: str
    outcome: str          # TP WV FN TN FF
    gt: object = None
    pred: object = None
    anls: float | None = None
    canonical: bool | None = None   # non-null prediction in the requested form (see normalize.is_canonical)
    matched_by: str = ""            # TP through answers.json: "accepted" or "from:<field>"; "" otherwise


@dataclass
class DocScore:
    fields: list[FieldResult] = field(default_factory=list)
    rows: dict = field(default_factory=dict)   # list field -> {"tp","fp","fn"} cell counts
    schema_echo: bool = False
    json_valid: bool = True


def outcome(fname: str, gt, pred, accepted=None, rules=N.RULES) -> FieldResult:
    gnull, pnull = N.is_null(gt), N.is_null(pred)
    if gnull and pnull:
        return FieldResult(fname, "TN", gt, pred)
    if gnull:
        return FieldResult(fname, "FF", gt, pred, canonical=N.is_canonical(fname, pred))
    if pnull:
        return FieldResult(fname, "FN", gt, pred, anls=0.0)
    ok, via = N.equal(fname, gt, pred, rules), ""
    if not ok and any(N.equal(fname, a, pred, rules) for a in accepted or ()):
        ok, via = True, "accepted"
    canon = N.is_canonical(fname, pred)
    if ok and fname in N.NAME_FIELDS:
        # correct name: canonical only if it is a GT / accepted name itself, not the name inside extra text
        canon = any(N.name_clean(v, pred, rules) for v in [gt, *(accepted or ())] if not N.is_null(v))
    return FieldResult(fname, "TP" if ok else "WV", gt, pred, anls=1.0 if ok else N.anls(gt, pred),
                       canonical=canon, matched_by=via)


def field_outcome(fname: str, spec: dict, pred: dict, rules=N.RULES) -> FieldResult:
    """One field of answers.json (`spec`: answer, accepted, accept_from) against a whole parsed prediction."""
    r = outcome(fname, spec.get("answer"), unwrap(pred.get(fname)), spec.get("accepted"), rules)
    if r.outcome in ("WV", "FN"):
        for other in spec.get("accept_from") or ():
            p2 = unwrap(pred.get(other))
            if not N.is_null(p2) and N.equal(fname, spec["answer"], p2, rules):
                r.outcome, r.anls, r.matched_by = "TP", 1.0, f"from:{other}"
                break
    return r


def unwrap(v):
    """P2 prompts return {"value": .., "quote": ..}; take the value."""
    if isinstance(v, dict) and "value" in v:
        return v["value"]
    return v


def _row_sim(g: dict, p: dict) -> float:
    keys = set(g) | set(p)
    if not keys:
        return 0.0
    s = 0.0
    for k in keys:
        gv, pv = g.get(k), unwrap(p.get(k)) if isinstance(p, dict) else None
        if N.is_null(gv) and N.is_null(pv):
            s += 1
        elif not N.is_null(gv) and not N.is_null(pv):
            s += 1.0 if N.equal(k, gv, pv) else N.anls(gv, pv)
    return s / len(keys)


def score_rows(gt_rows: list, pred_rows, skip=None) -> dict:
    """Cell-level TP/FP/FN after optimal row matching.
    skip: iterable of (row_index, key) GT cells that are not printed in the document (hygiene) -> not scored."""
    skip = {(int(i), k) for i, k in (skip or [])}
    gt_rows = gt_rows or []
    pred_rows = [r for r in (pred_rows or []) if isinstance(r, dict)]
    tp = fp = fn = 0
    if gt_rows and pred_rows:
        cost = np.array([[1 - _row_sim(g, p) for p in pred_rows] for g in gt_rows])
        gi, pi = linear_sum_assignment(cost)
        matched_g, matched_p = set(gi), set(pi)
        for a, b in zip(gi, pi):
            g, p = gt_rows[a], pred_rows[b]
            for k in g:
                if (int(a), k) in skip:
                    continue
                r = outcome(k, g.get(k), unwrap(p.get(k)))
                tp += r.outcome == "TP"
                fp += r.outcome in ("WV", "FF")
                fn += r.outcome in ("WV", "FN")
    else:
        matched_g, matched_p = set(), set()
    for i, g in enumerate(gt_rows):
        if i not in matched_g:
            fn += sum(not N.is_null(v) and (i, k) not in skip for k, v in g.items())
    for j, p in enumerate(pred_rows):
        if j not in matched_p:
            fp += sum(not N.is_null(unwrap(v)) for v in p.values())
    return {"tp": tp, "fp": fp, "fn": fn, "n_gt": len(gt_rows), "n_pred": len(pred_rows)}


def detect_schema_echo(pred: dict, schema: dict) -> bool:
    """VAREX 'schema echo': output repeats schema/type words instead of values."""
    vals = [unwrap(v) for k, v in pred.items() if k not in LIST_FIELDS]
    vals = [str(v).lower() for v in vals if not N.is_null(v)]
    if not vals:
        return False
    junk = sum(v in {"string", "number", "null", "string or null", "yyyy-mm-dd", "object", "array"} or
               v.startswith("{\"type\"") for v in vals)
    return junk / len(vals) >= 0.5


def score_doc(gt: dict, pred: dict | None, scored_fields: list[str] | None = None, schema: dict | None = None,
              row_skip: dict | None = None) -> DocScore:
    """gt: canonical ground truth (null = absent). scored_fields: limit to fields the dataset annotates reliably."""
    ds = DocScore()
    if pred is None:
        ds.json_valid = False
        pred = {}
    fields = scored_fields or [k for k in gt if k not in LIST_FIELDS]
    for f in fields:
        if f in LIST_FIELDS:
            continue
        ds.fields.append(outcome(f, gt.get(f), unwrap(pred.get(f))))
    for lf in LIST_FIELDS:
        if lf in gt and gt[lf] is not None and (scored_fields is None or lf in scored_fields):
            ds.rows[lf] = score_rows(gt[lf], pred.get(lf), (row_skip or {}).get(lf))
    if schema is not None:
        ds.schema_echo = detect_schema_echo(pred, schema)
    return ds


def score_answers(answers: dict, pred: dict | None, schema: dict | None = None) -> DocScore:
    """Score one model output against final/docs/<id>/answers.json. Only fields listed there are scored;
    other keys the model returns are ignored (but may count for a field through `accept_from`)."""
    ds = DocScore()
    if not isinstance(pred, dict):
        ds.json_valid = False
        pred = {}
    for f, spec in answers["fields"].items():
        if f not in LIST_FIELDS:
            ds.fields.append(field_outcome(f, spec, pred))
    if schema is not None:
        ds.schema_echo = detect_schema_echo(pred, schema)
    return ds


_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def parse_json(text: str):
    """Best-effort JSON extraction from model output. Returns (obj|None, strict_ok: bool)."""
    if text is None:
        return None, False
    t = text.strip()
    t = re.sub(r"<think>.*?</think>", "", t, flags=re.S).strip()
    try:
        return json.loads(t), True
    except Exception:
        pass
    m = _FENCE.search(t)
    if m:
        try:
            return json.loads(m.group(1)), False
        except Exception:
            pass
    a, b = t.find("{"), t.rfind("}")
    if a != -1 and b > a:
        try:
            return json.loads(t[a:b + 1]), False
        except Exception:
            pass
    return None, False
