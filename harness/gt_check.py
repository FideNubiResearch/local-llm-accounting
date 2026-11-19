"""GT / input checker: use the round-1 model results to find suspect ground truth, documents, definitions and scoring.

  uv run python -m harness.gt_check [--runs-from protocol/round1.json] [--out reports/gt_check]
      [--fields-root runs] [--fields-name fields.csv] [--n-rows N] [--carry-verdicts PATH ...]

--fields-root / --fields-name: where each run's scored fields are read, <fields-root>/<run_id>/<fields-name>, with
summary.md next to it (e.g. a re-score: --fields-root reports/rescore_r1). config.json is always read from runs/.
GT edits applied after round 1 (reports/gt_check/applied_fixes.csv: fix / exclude) are tolerated when fields.csv
still holds the old answer, so the round-1 fields.csv stay loadable; so are documents excluded as a whole
(exclude_doc, field "*"): their rows are tolerated although final/docs/<doc> is gone.
--carry-verdicts: verdict files of earlier checks, any number (default: CARRY_DEFAULT = the round-1 review
reports/gt_check/review/verdicts.jsonl, the closeout stage-2 review reports/gt_check/stage2/verdicts.jsonl and the r1b
review reports/gt_check/r1b/verdicts.jsonl;
missing files are skipped; a later file wins for the same review_id). Their verdicts are carried over by review_id, so pairs already reviewed are marked on a new run (suspects.csv `verdict`,
`verdict_source`; review/queue.csv `prior_verdict`). The --out directory's own review/verdicts.jsonl wins.

Specification: reports/gt_check/PLAN.md. A (doc, field) key is
  L1  every voting model is wrong (and at least 5 models vote),
  L2  more than half of the voting models are wrong (and not L1),
  L0  otherwise.
Wrong = outcome WV / FN / FF (harness/score.py); a model whose output for a document was not valid JSON abstains on
all of that document's fields. The "raw" variant (baseline of PLAN section A) counts the scored outcomes of all
6 models, i.e. an invalid-JSON doc's FN rows are wrong and its TN rows are not.

Read-only over runs/ and final/; deterministic; no network; writes only into the --out directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd
import yaml
from rapidfuzz.distance import Levenshtein

from harness import normalize as N
from harness import score as S

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "final"

N_RUNS, N_DOCS, N_ROWS = 6, 1574, 14561
WRONG = {"WV", "FN", "FF"}
CORRECT = {"TP", "TN"}
OUTCOMES = ("TP", "WV", "FN", "TN", "FF")
NULL_KEY = "<NULL>"
LEVELS = ("L1", "L2", "L0")
LEVEL_ORDER = {lv: i for i, lv in enumerate(LEVELS)}
HINTS = ("sibling_copy", "scorer_strict", "gt_value_suspect", "gt_null_suspect", "mask_leak", "value_not_found",
         "scattered")
HINT_ORDER = {h: i for i, h in enumerate(HINTS)}
PATTERNS = ("consensus_alt", "consensus_null", "scattered")
ERR_TYPES = ("WV", "FN", "FF_probe", "FF_mask")
STRONG_PAIR = ("qwen3.5-9b", "gemma4-12b")
TWIN_SUFFIX = re.compile(r"__(clean|photo|digital|scan|mask)$")
META = ["source", "kind", "lang", "doc_type", "variant", "template", "masked", "gt"]
VERDICTS = ("gt_wrong", "gt_null_wrong", "gt_value_absent", "doc_unreadable", "doc_mismatch", "mask_leak",
            "definition_ambiguity", "scorer_too_strict", "model_failure", "unsure", "ok")
FIX_VERDICTS = {"gt_wrong", "gt_null_wrong", "gt_value_absent"}
BATCH = 25
CARRY_DEFAULT = ("reports/gt_check/review/verdicts.jsonl", "reports/gt_check/stage2/verdicts.jsonl",
                 "reports/gt_check/r1b/verdicts.jsonl")


class CheckError(Exception):
    """An input check failed; the analysis must not continue."""


# ----------------------------------------------------------------------------------------------------------------
# pure helpers (tested in tests/test_gt_check.py)
# ----------------------------------------------------------------------------------------------------------------
def model_short(run_id: str) -> str:
    return run_id.split("__")[1]


def level(n_wrong: int, n_voting: int) -> str:
    if n_voting >= 5 and n_wrong == n_voting:
        return "L1"
    if n_voting > 0 and n_wrong / n_voting > 0.5:
        return "L2"
    return "L0"


def is_wrong(outcome: str) -> bool:
    """Only the outcome decides; `canonical` (answer format) is a signal, never a mistake."""
    return outcome in WRONG


def err_type(gt: str, field_masked: bool, wrong_outcomes: list[str]) -> str:
    """Error type of a key from the outcomes of its wrong voters ("" when nobody is wrong).
    Value GT: the majority of WV vs FN (tie -> WV). Null GT: FF_mask for a painted-over field, else FF_probe."""
    if not wrong_outcomes:
        return ""
    if gt == "":
        return "FF_mask" if field_masked else "FF_probe"
    c = Counter(wrong_outcomes)
    return "WV" if c["WV"] >= c["FN"] else "FN"


def decode_pred(s: str):
    """fields.csv `pred` is a JSON dump of the model value; empty = null."""
    if s is None or s == "":
        return None
    try:
        return json.loads(s)
    except (TypeError, ValueError):
        return s


def display(v) -> str:
    """A decoded prediction as a CSV cell: strings as is, other JSON values dumped, null empty."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False)


def _raw(v) -> str:
    return v if isinstance(v, str) else display(v)


def _kind(field: str) -> str:
    return N.FIELD_KIND.get(field, "text")


def _amount(v) -> Decimal | None:
    if isinstance(v, bool):
        return None
    try:
        return N.amount(v)
    except (InvalidOperation, ValueError, TypeError):
        return None


def canon_key(field: str, pred) -> str:
    """Cluster key of a prediction: null -> <NULL>; otherwise the field kind's normalized form."""
    if N.is_null(pred):
        return NULL_KEY
    kind, raw = _kind(field), _raw(pred)
    try:
        if kind == "amount":
            a = _amount(pred)
            if a is not None:
                return str(a.quantize(Decimal("0.01")))
        elif kind == "date":
            ds = sorted(d.isoformat() for d in N.dates(raw))
            if ds:
                return "|".join(ds)
        elif kind == "time":
            t = N.time_hm(raw)
            if t:
                return t
        elif kind == "id":
            i = N.ident_value(raw)
            if i:
                return i
        elif kind == "currency":
            c = N.currency(raw)
            if c:
                return c
    except (InvalidOperation, ValueError, TypeError, ArithmeticError):
        pass
    return N.text(raw)


def safe_equal(field: str, gt, pred) -> bool:
    """normalize.equal with the first argument treated as canonical; False where it cannot be parsed."""
    if N.is_null(gt) or N.is_null(pred):
        return False
    try:
        return bool(N.equal(field, gt, _raw(pred)))
    except Exception:  # noqa: BLE001 - equal() parses gt strictly and raises on non-canonical input
        return False


def cluster_preds(field: str, preds: list[tuple[str, object]]) -> list[dict]:
    """Cluster the (model, pred) pairs of the wrong voters.
    Exact canon_key groups first, then groups are merged when normalize.equal(field, key_a, pred_b) holds.
    Nulls form their own cluster. Returns clusters sorted by size desc, then key asc (deterministic):
    {"key", "models", "preds"}; key = the member key group with most members (tie: smallest)."""
    groups: dict[str, list[tuple[str, object]]] = defaultdict(list)
    for m, p in preds:
        groups[canon_key(field, p)].append((m, p))
    keys = sorted(groups)
    parent = {k: k for k in keys}

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    nonnull = [k for k in keys if k != NULL_KEY]
    for i, a in enumerate(nonnull):
        for b in nonnull[i + 1:]:
            if find(a) == find(b):
                continue
            if any(safe_equal(field, a, p) for _, p in groups[b]) or any(safe_equal(field, b, p) for _, p in groups[a]):
                ra, rb = find(a), find(b)
                parent[max(ra, rb)] = min(ra, rb)
    merged: dict[str, list[str]] = defaultdict(list)
    for k in keys:
        merged[find(k)].append(k)
    out = []
    for ks in merged.values():
        rep = sorted(ks, key=lambda k: (-len(groups[k]), k))[0]
        members = [mp for k in ks for mp in groups[k]]
        out.append({"key": rep, "models": [m for m, _ in members], "preds": [p for _, p in members]})
    out.sort(key=lambda c: (-len(c["models"]), c["key"]))
    return out


def cluster_example(cluster: dict):
    """Most common raw prediction in a cluster (tie: smallest display string)."""
    cnt = Counter(display(p) for p in cluster["preds"])
    best = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return next(p for p in cluster["preds"] if display(p) == best)


def _strip_cc(s: str) -> str:
    return re.sub(r"^[A-Z]{2}(?=[0-9])", "", N.ident_value(s))


def id_prefix_only(gt, pred) -> bool:
    """Equal after removing a leading 2-letter country code (PT510776914 vs 510776914), but not equal as is."""
    if N.is_null(gt) or N.is_null(pred):
        return False
    a, b = _strip_cc(_raw(gt)), _strip_cc(_raw(pred))
    return bool(a) and a == b and N.ident_value(_raw(gt)) != N.ident_value(_raw(pred))


def digit_edit1(field: str, gt, pred) -> bool:
    """Amount / id that differs from the GT by exactly one digit edit (377859 vs 377059)."""
    if N.is_null(gt) or N.is_null(pred):
        return False
    kind = _kind(field)
    if kind == "amount":
        a, b = _amount(gt), _amount(pred)
        if a is None or b is None:
            return False
        da, db = (re.sub(r"\D", "", str(x.quantize(Decimal("0.01")))) for x in (a, b))
    elif kind == "id":
        da, db = N.ident_value(_raw(gt)), N.ident_value(_raw(pred))
    else:
        return False
    return bool(da) and bool(db) and Levenshtein.distance(da, db) == 1


def substring_signals(field: str, gt, pred) -> tuple[bool, bool]:
    """(gt_in_pred, pred_in_gt) on normalize.text; only for text and id fields (for amounts/dates a substring
    such as "15" in "150" is meaningless)."""
    if N.is_null(gt) or N.is_null(pred) or _kind(field) not in ("text", "id"):
        return False, False
    g, p = N.text(_raw(gt)), N.text(_raw(pred))
    if not g or not p or g == p:
        return False, False
    return g in p, p in g


def consensus_eq_field(field: str, pred, doc_gts: dict[str, str]) -> str:
    """Other fields of the same doc (same field kind) whose GT equals the prediction (subtotal = total, id swaps)."""
    if N.is_null(pred):
        return ""
    kind = _kind(field)
    hits = [f for f, g in sorted(doc_gts.items())
            if f != field and g != "" and _kind(f) == kind and safe_equal(f, g, pred)]
    return ";".join(hits)


def twin_group(doc_id: str, base_doc: str = "") -> str:
    """Doc id without its variant suffix (__clean/__photo/__digital/__scan/__mask), or manifest base_doc."""
    g = base_doc or doc_id
    while TWIN_SUFFIX.search(g):
        g = TWIN_SUFFIX.sub("", g)
    return g


def pattern_of(n_wrong: int, n_agree: int, key: str) -> str:
    if n_wrong == 0:
        return ""
    if n_agree >= 4:
        return "consensus_null" if key == NULL_KEY else "consensus_alt"
    return "scattered"


def hint_of(row: dict) -> str:
    """First matching hint (orders the review queue only; not a verdict)."""
    if row["n_wrong"] == 0:
        return ""
    if row["consensus_eq_field"]:
        return "sibling_copy"
    anls_hi = _kind(row["field"]) == "text" and row["anls_consensus"] not in (None, "") and row["anls_consensus"] >= 0.9
    if row["gt_in_pred"] or row["pred_in_gt"] or row["id_prefix_only"] or anls_hi:
        return "scorer_strict"
    et, pat = row["err_type"], row["pattern"]
    if et == "WV" and (pat == "consensus_alt" or row["digit_edit1"]):
        return "gt_value_suspect"
    if et == "FF_probe" and pat == "consensus_alt":
        return "gt_null_suspect"
    if et == "FF_mask" and row["n_agree"] >= 4:
        return "mask_leak"
    if et == "FN" and pat == "consensus_null":
        return "value_not_found"
    return "scattered"


_SEP = re.compile(r"^\|?\s*:?-{3,}")


def parse_summary_all(text: str) -> pd.DataFrame:
    """The "## All" markdown table of a run's summary.md (harness/report.py) as a DataFrame of strings."""
    lines = text.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.strip() == "## All")
    except StopIteration as e:
        raise CheckError("summary.md has no '## All' section") from e
    rows = []
    for ln in lines[start + 1:]:
        s = ln.strip()
        if s.startswith("## "):
            break
        if not s.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        rows.append(cells)
    if len(rows) < 2:
        raise CheckError("summary.md '## All' table is empty")
    return pd.DataFrame(rows[1:], columns=rows[0])


def outcome_counts(df: pd.DataFrame, by: str = "doc_type") -> pd.DataFrame:
    c = df.groupby(by)["outcome"].value_counts().unstack(fill_value=0)
    for o in OUTCOMES:
        if o not in c:
            c[o] = 0
    return c[list(OUTCOMES)].astype(int)


def reconcile(run_id: str, df: pd.DataFrame, summary_text: str) -> pd.DataFrame:
    """Per doc_type: summary wrong==WV, missed==FN, values==TP+WV+FN, nulls==TN+FF."""
    summ = parse_summary_all(summary_text).set_index("doc_type")
    calc = outcome_counts(df)
    rows = []
    for dt in sorted(set(summ.index) | set(calc.index)):
        c = calc.loc[dt] if dt in calc.index else pd.Series(0, index=list(OUTCOMES))
        s = summ.loc[dt] if dt in summ.index else None
        exp = {"values": c.TP + c.WV + c.FN, "wrong": c.WV, "missed": c.FN, "nulls": c.TN + c.FF}
        got = {k: (int(float(s[k])) if s is not None else None) for k in exp}
        rows.append({"run_id": run_id, "doc_type": dt, **{f"{k}_summary": got[k] for k in exp},
                     **{f"{k}_fields": int(exp[k]) for k in exp}, "ok": all(got[k] == exp[k] for k in exp)})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------------------------------------------
# loading + input checks
# ----------------------------------------------------------------------------------------------------------------
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def applied_fixes(root: Path) -> tuple[dict, set]:
    """GT edits made after round 1: {(doc, field): (old, new)} for fixes and {(doc, field)} for exclusions
    (a whole excluded document appears as (doc, "*"))."""
    path = root / "reports" / "gt_check" / "applied_fixes.csv"
    if not path.exists():
        return {}, set()
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    fixes = {(r.doc_id, r.field): (r.old, r.new) for r in df.itertuples() if r.action == "fix"}
    excl = {(r.doc_id, r.field) for r in df.itertuples() if r.action in ("exclude", "exclude_doc")}
    return fixes, excl


def reproduce(rdir: Path, df: pd.DataFrame, answers: dict) -> int:
    """Rows of a fields.csv whose outcome the current scorer and answers.json do not reproduce.
    With predictions.jsonl (a real run) every document is re-scored from the raw model output; otherwise each row is
    re-scored from its own `pred` (accept_from cannot be checked then)."""
    got = {}
    ppath = rdir / "predictions.jsonl"
    if ppath.exists():
        for line in ppath.read_text().splitlines():
            if not line.strip():
                continue
            p = json.loads(line)
            if p["doc_id"] in answers:
                for r in S.score_answers(answers[p["doc_id"]], p["parsed"]).fields:
                    got[(p["doc_id"], r.field)] = r.outcome
    bad = 0
    for doc, fld, pred, o in zip(df["doc_id"], df["field"], df["pred"], df["outcome"]):
        if (doc, fld) in got:
            new = got[(doc, fld)]
        else:
            spec = answers.get(doc, {}).get("fields", {}).get(fld)
            if spec is None:
                bad += 1
                continue
            new = S.field_outcome(fld, spec, {fld: decode_pred(pred)}).outcome
        bad += new != o
    return bad


def load(root: Path = ROOT, protocol: Path | None = None, n_runs: int = N_RUNS, n_docs: int = N_DOCS,
         n_rows: int | None = N_ROWS, fields_root: Path | None = None, fields_name: str = "fields.csv",
         n_docs_fields: int | None = None) -> dict:
    """Load all runs, check them (raise CheckError on failure) and build the wide per-key table.
    n_rows=None: expect as many rows as final/ answers.json hold fields now (a re-score).
    n_docs: documents the runs selected (config.json); n_docs_fields: documents in fields.csv (default n_docs; a
    re-score has fewer when documents were excluded after the run)."""
    protocol = protocol or root / "protocol" / "round1.json"
    fields_root = fields_root or root / "runs"
    n_docs_fields = n_docs if n_docs_fields is None else n_docs_fields
    answers_cache: dict[str, dict] = {}
    fixes, excluded = applied_fixes(root)

    def answers(doc):
        if doc not in answers_cache:
            path = root / "final" / "docs" / doc / "answers.json"
            if not path.exists() and (doc, "*") in excluded:     # whole document excluded after round 1
                answers_cache[doc] = {"doc_id": doc, "pages": [], "fields": {}}
            else:
                answers_cache[doc] = json.loads(path.read_text())
        return answers_cache[doc]
    proto = json.loads(Path(protocol).read_text())
    runs = proto["runs"]
    if len(runs) != n_runs:
        raise CheckError(f"{protocol}: {len(runs)} runs, expected {n_runs}")
    info, frames = [], {}
    for r in runs:
        rid = r["run_id"]
        m = model_short(rid)
        rdir = root / "runs" / rid
        cfg = json.loads((rdir / "config.json").read_text())
        if cfg.get("n_selected") != n_docs:
            raise CheckError(f"{rid}: n_selected={cfg.get('n_selected')}, expected {n_docs}")
        fpath = fields_root / rid / fields_name
        df = pd.read_csv(fpath, dtype=str, keep_default_na=False)
        if n_rows is None:
            n_rows = sum(len(answers(d)["fields"]) for d in df["doc_id"].unique())
        if len(df) != n_rows:
            raise CheckError(f"{rid}: fields.csv has {len(df)} rows, expected {n_rows}")
        if df.duplicated(["doc_id", "field"]).any():
            raise CheckError(f"{rid}: duplicate (doc_id, field) keys")
        if df["doc_id"].nunique() != n_docs_fields:
            raise CheckError(f"{rid}: {df['doc_id'].nunique()} docs, expected {n_docs_fields}")
        bad_err = df["error"].ne("").sum()
        frames[m] = df.sort_values(["doc_id", "field"]).reset_index(drop=True)
        info.append({"run_id": rid, "model": m, "hf_model": r.get("model", cfg.get("model")),
                     "revision": cfg.get("revision", r.get("revision")), "protocol_revision": r.get("revision"),
                     "fields_path": str(fpath), "fields_sha256": sha256(fpath), "rows": len(df),
                     "error_rows": int(bad_err), "summary": (fpath.parent / "summary.md").read_text(),
                     "rdir": rdir})
    models = [i["model"] for i in info]
    if len(set(models)) != len(models):
        raise CheckError(f"model short names not unique: {models}")
    base = frames[models[0]]
    for m in models[1:]:
        f = frames[m]
        if not (f["doc_id"].equals(base["doc_id"]) and f["field"].equals(base["field"])):
            raise CheckError(f"{m}: key set differs from {models[0]}")
        for col in META:
            if not f[col].equals(base[col]):
                raise CheckError(f"{m}: column {col!r} differs from {models[0]}")
    recon = pd.concat([reconcile(i["run_id"], frames[i["model"]], i["summary"]) for i in info], ignore_index=True)

    wide = base[["doc_id", "field"] + META].copy()
    for m in models:
        f = frames[m]
        wide[f"outcome_{m}"] = f["outcome"]
        wide[f"predraw_{m}"] = f["pred"]
        wide[f"canonical_{m}"] = f["canonical"]
        wide[f"abstain_{m}"] = f["json_valid"].eq("False")

    # answers.json: printed, per-field mask, pages; GT must match fields.csv
    man = pd.read_csv(root / "final" / "manifest.csv", dtype=str, keep_default_na=False).set_index("doc_id")
    printed, fmask, pages = [], [], {}
    mismatches = []
    tolerated = 0
    for doc, field, gt in zip(wide["doc_id"], wide["field"], wide["gt"]):
        if doc not in pages:
            pages[doc] = ";".join(str((root / "final" / "docs" / doc / p).resolve())
                                  for p in answers(doc).get("pages", []))
        fa = answers(doc)["fields"].get(field)
        if fa is None:
            if (doc, field) in excluded or (doc, "*") in excluded:     # excluded from scoring after round 1
                tolerated += 1
            else:
                mismatches.append(f"{doc}::{field} missing in answers.json")
            printed.append(""); fmask.append(False)
            continue
        if str(fa.get("answer") or "") != gt:
            if fixes.get((doc, field)) == (gt, str(fa.get("answer") or "")):
                tolerated += 1                           # journaled GT fix after round 1
            else:
                mismatches.append(f"{doc}::{field} answers.json={fa.get('answer')!r} fields.csv={gt!r}")
        printed.append(display(fa.get("printed")))
        fmask.append(bool(fa.get("masked", False)))
    if mismatches:
        raise CheckError(f"{len(mismatches)} GT mismatches between answers.json and fields.csv, e.g. {mismatches[:3]}")
    wide["printed"] = printed
    wide["field_masked"] = fmask
    wide["page_paths"] = wide["doc_id"].map(pages)
    wide["base_doc"] = wide["doc_id"].map(lambda d: man.at[d, "base_doc"] if d in man.index else "")
    reproduce_bad = {i["model"]: reproduce(i["rdir"], frames[i["model"]], {d: answers(d) for d in pages})
                     for i in info}
    for i in info:
        i.pop("summary")
        i.pop("rdir")
    return {"wide": wide, "models": models, "runs": info, "recon": recon, "frames": frames,
            "gt_edits_tolerated": tolerated, "reproduce_mismatches": reproduce_bad}


# ----------------------------------------------------------------------------------------------------------------
# per-key analysis
# ----------------------------------------------------------------------------------------------------------------
def analyze(wide: pd.DataFrame, models: list[str]) -> pd.DataFrame:
    """One row per (doc, field) with votes, level, consensus, signals and hint (votes.csv columns)."""
    doc_gts: dict[str, dict[str, str]] = defaultdict(dict)
    for d, f, g in zip(wide["doc_id"], wide["field"], wide["gt"]):
        doc_gts[d][f] = g
    rows = []
    for rec in wide.to_dict("records"):
        field, gt = rec["field"], rec["gt"]
        outs = {m: rec[f"outcome_{m}"] for m in models}
        preds = {m: decode_pred(rec[f"predraw_{m}"]) for m in models}
        abst = {m: bool(rec[f"abstain_{m}"]) for m in models}
        voters = [m for m in models if not abst[m]]
        wrong = [m for m in voters if is_wrong(outs[m])]
        # raw = baseline (PLAN A): outcomes as scored over all 6 models; an invalid-JSON doc is scored FN/TN by
        # harness.score, so its FN rows count as wrong and its (rare) TN rows do not.
        n_wrong_raw = sum(is_wrong(outs[m]) for m in models)
        clusters = cluster_preds(field, [(m, preds[m]) for m in wrong])
        cons = clusters[0] if clusters else None
        ex = cluster_example(cons) if cons else None
        cons_null = cons is not None and cons["key"] == NULL_KEY
        n_agree = len(cons["models"]) if cons else 0
        row = {
            "doc_id": rec["doc_id"], "field": field, "review_id": f"{rec['doc_id']}::{field}",
            "source": rec["source"], "kind": rec["kind"], "lang": rec["lang"], "doc_type": rec["doc_type"],
            "variant": rec["variant"], "template": rec["template"], "doc_masked": rec["masked"] == "True",
            "field_masked": bool(rec["field_masked"]), "twin_group": twin_group(rec["doc_id"], rec["base_doc"]),
            "gt": gt, "printed": rec["printed"], "n_voting": len(voters), "n_wrong": len(wrong),
            "n_wrong_raw": n_wrong_raw,
            "share": round(len(wrong) / len(voters), 4) if voters else None,
            "level": level(len(wrong), len(voters)), "level_raw": level(n_wrong_raw, len(models)),
            "err_type": err_type(gt, bool(rec["field_masked"]), [outs[m] for m in wrong]),
        }
        for m in models:
            row[f"outcome_{m}"] = outs[m]
        for m in models:
            row[f"pred_{m}"] = display(preds[m])
        for m in models:
            row[f"canonical_{m}"] = rec[f"canonical_{m}"]
        gin, ping = substring_signals(field, gt, ex) if cons and not cons_null else (False, False)
        an = None
        if cons and not cons_null and gt != "":
            try:
                an = round(N.anls(gt, _raw(ex)), 4)
            except Exception:  # noqa: BLE001
                an = None
        same = any(all(s in c["models"] for s in STRONG_PAIR) for c in clusters)
        row.update({
            "consensus_example": display(ex) if cons else "",
            "consensus_key": cons["key"] if cons else "",
            "n_agree": n_agree,
            "agree_share": round(n_agree / len(voters), 4) if voters else 0.0,
            "n_distinct_wrong": len(clusters),
            "consensus_models": ";".join(m for m in models if cons and m in cons["models"]),
            "pattern": pattern_of(len(wrong), n_agree, cons["key"] if cons else ""),
            "consensus_eq_field": consensus_eq_field(field, ex, doc_gts[rec["doc_id"]]) if cons else "",
            "gt_in_pred": gin, "pred_in_gt": ping, "anls_consensus": an,
            "digit_edit1": bool(cons) and not cons_null and digit_edit1(field, gt, ex),
            "id_prefix_only": bool(cons) and not cons_null and _kind(field) == "id" and id_prefix_only(gt, ex),
            "consensus_noncanonical": bool(cons) and not cons_null and not N.is_canonical(field, ex),
            "strong_pair_agree": same,
            "twin_levels": "",
        })
        row["hint"] = hint_of(row)
        row["page_paths"] = rec["page_paths"]
        rows.append(row)
    votes = pd.DataFrame(rows)
    # twin levels: levels of the same field in the other docs of the twin group
    lv = {(d, f): l for d, f, l in zip(votes["doc_id"], votes["field"], votes["level"])}
    members: dict[str, list[str]] = defaultdict(list)
    for d, g in votes[["doc_id", "twin_group"]].drop_duplicates().itertuples(index=False):
        members[g].append(d)
    votes["twin_levels"] = [
        ";".join(f"{o}:{lv[(o, f)]}" for o in sorted(members[g]) if o != d and (o, f) in lv)
        for d, f, g in zip(votes["doc_id"], votes["field"], votes["twin_group"])]
    return sort_votes(votes)


def vote_columns(models: list[str]) -> list[str]:
    return (["doc_id", "field", "review_id", "source", "kind", "lang", "doc_type", "variant", "template",
             "doc_masked", "field_masked", "twin_group", "gt", "printed", "n_voting", "n_wrong", "n_wrong_raw",
             "share", "level", "level_raw", "err_type"]
            + [f"outcome_{m}" for m in models] + [f"pred_{m}" for m in models] + [f"canonical_{m}" for m in models]
            + ["consensus_example", "consensus_key", "n_agree", "agree_share", "n_distinct_wrong", "consensus_models",
               "pattern", "consensus_eq_field", "gt_in_pred", "pred_in_gt", "anls_consensus", "digit_edit1",
               "id_prefix_only", "consensus_noncanonical", "strong_pair_agree", "twin_levels", "hint", "page_paths"])


def sort_votes(v: pd.DataFrame) -> pd.DataFrame:
    v = v.assign(_lv=v["level"].map(LEVEL_ORDER))
    v = v.sort_values(["_lv", "agree_share", "source", "doc_id", "field"], ascending=[True, False, True, True, True],
                      kind="mergesort")
    return v.drop(columns="_lv").reset_index(drop=True)


def sort_suspects(s: pd.DataFrame) -> pd.DataFrame:
    s = s.assign(_lv=s["level"].map(LEVEL_ORDER), _h=s["hint"].map(HINT_ORDER))
    s = s.sort_values(["_lv", "_h", "n_agree", "source", "doc_id", "field"],
                      ascending=[True, True, False, True, True, True], kind="mergesort")
    return s.drop(columns=["_lv", "_h"]).reset_index(drop=True)


# ----------------------------------------------------------------------------------------------------------------
# group tables
# ----------------------------------------------------------------------------------------------------------------
def group_table(v: pd.DataFrame, by: list[str], overall: float) -> pd.DataFrame:
    rows = []
    for key, g in v.groupby(by, dropna=False, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        susp = g[g["level"].isin(["L1", "L2"])]
        n1, n2 = int((g["level"] == "L1").sum()), int((g["level"] == "L2").sum())
        rate = (n1 + n2) / len(g)
        r = dict(zip(by, key))
        r.update({"n_keys": len(g), "n_L1": n1, "n_L2": n2, "n_suspect": n1 + n2, "suspect_rate": round(rate, 4),
                  "base_err_rate": round(g["n_wrong"].mean() / N_RUNS, 4)})
        for p in PATTERNS:
            r[f"pattern_{p}"] = int((susp["pattern"] == p).sum())
        for h in HINTS:
            r[f"hint_{h}"] = int((susp["hint"] == h).sum())
        r["lift"] = round(rate / overall, 3) if overall else None
        rows.append(r)
    return pd.DataFrame(rows).sort_values(["n_suspect", "lift"] + by, ascending=[False, False] + [True] * len(by),
                                          kind="mergesort").reset_index(drop=True)


GROUPS = {
    "by_field": ["field"], "by_source_field": ["source", "field"], "by_source": ["source"], "by_lang": ["lang"],
    "by_doc_type": ["doc_type"], "by_variant": ["variant"], "by_kind": ["kind"], "by_field_masked": ["field_masked"],
}
EDB = "eurodocbench"


def group_tables(v: pd.DataFrame) -> dict[str, pd.DataFrame]:
    overall = v["level"].isin(["L1", "L2"]).mean()
    out = {name: group_table(v, by, overall) for name, by in GROUPS.items()}
    edb = v[v["source"] == EDB]
    if len(edb):
        out["by_template"] = group_table(edb, ["template"], overall)
        out["by_lang_field_edb"] = group_table(edb, ["lang", "field"], overall)
    else:
        out["by_template"] = pd.DataFrame()
        out["by_lang_field_edb"] = pd.DataFrame()
    return out


def docs_table(v: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for doc, g in v.groupby("doc_id", sort=True):
        susp = g[g["level"].isin(["L1", "L2"])]
        n1, n2 = int((g["level"] == "L1").sum()), int((g["level"] == "L2").sum())
        ns = n1 + n2
        weak = int(susp["hint"].isin(["scattered", "value_not_found"]).sum())
        first = g.iloc[0]
        hints = Counter(susp["hint"])
        rows.append({"doc_id": doc, "source": first["source"], "lang": first["lang"], "doc_type": first["doc_type"],
                     "variant": first["variant"], "n_fields": len(g), "n_L1": n1, "n_L2": n2, "n_suspect": ns,
                     "suspect_share": round(ns / len(g), 4),
                     "hints": ";".join(f"{h}:{hints[h]}" for h in HINTS if hints[h]),
                     "doc_problem": ns >= 2 and (ns / len(g) >= 0.5 or weak / ns >= 0.5),
                     "twin_group": first["twin_group"], "page_paths": first["page_paths"]})
    d = pd.DataFrame(rows)
    by_group = d.groupby("twin_group")
    clean_ok = []
    for doc, grp, in zip(d["doc_id"], d["twin_group"]):
        others = by_group.get_group(grp)
        others = others[others["doc_id"] != doc]
        clean_ok.append("" if others.empty else bool((others["n_suspect"] == 0).any()))
    d["twin_clean_ok"] = clean_ok
    d = d[["doc_id", "source", "lang", "doc_type", "variant", "n_fields", "n_L1", "n_L2", "n_suspect",
           "suspect_share", "hints", "doc_problem", "twin_group", "twin_clean_ok", "page_paths"]]
    return d.sort_values(["suspect_share", "n_suspect", "doc_id"], ascending=[False, False, True],
                         kind="mergesort").reset_index(drop=True)


CLUSTER_KEY = ["source", "field", "err_type", "hint"]


def clusters_table(susp: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for key, g in susp.groupby(CLUSTER_KEY, sort=True):
        sib = Counter(x for x in g["consensus_eq_field"] if x)
        ex = list(g["review_id"][:3]) + ["", "", ""]
        rows.append({**dict(zip(CLUSTER_KEY, key)), "count": len(g), "n_L1": int((g["level"] == "L1").sum()),
                     "example_1": ex[0], "example_2": ex[1], "example_3": ex[2],
                     "sibling_field_mode": sorted(sib.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if sib else ""})
    cols = CLUSTER_KEY + ["count", "n_L1", "example_1", "example_2", "example_3", "sibling_field_mode"]
    if not rows:
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(rows)[cols].sort_values(["count", "n_L1"] + CLUSTER_KEY,
                                                ascending=[False, False] + [True] * 4,
                                                kind="mergesort").reset_index(drop=True)


# ----------------------------------------------------------------------------------------------------------------
# review queue + verdicts
# ----------------------------------------------------------------------------------------------------------------
def merge_verdicts(carried: list[Path], own: Path) -> tuple[dict[str, dict], int]:
    """Verdicts carried over from earlier checks (by review_id, later files win) overlaid by the --out directory's
    own verdicts.jsonl. Each record gets `_source`: the file it came from. Returns (verdicts, unreadable lines)."""
    out, bad = {}, 0
    paths = [p for p in carried if Path(p).resolve() != Path(own).resolve()] + [own]
    for p in paths:
        v, b = read_verdicts(Path(p))
        bad += b
        for rid, rec in v.items():
            out[rid] = {**rec, "_source": str(p)}
    return out, bad


def read_verdicts(path: Path) -> tuple[dict[str, dict], int]:
    """Latest verdict per review_id (file order) and the number of unreadable lines."""
    out, bad = {}, 0
    if not path.exists():
        return out, bad
    for ln in path.read_text().splitlines():
        if not ln.strip():
            continue
        try:
            rec = json.loads(ln)
        except ValueError:
            bad += 1
            continue
        if not isinstance(rec, dict) or "review_id" not in rec:
            bad += 1
            continue
        out[rec["review_id"]] = rec
    return out, bad


def build_queue(v: pd.DataFrame, susp: pd.DataFrame, docs: pd.DataFrame, models: list[str],
                field_human: dict[str, str], verdicts: dict | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Review queue (PLAN section 6) and the hidden controls key. `prior_verdict`: a verdict already given for the
    pair (carried over by review_id), so a reviewer can skip it."""
    verdicts = verdicts or {}
    order: list[tuple[str, int]] = []
    seen: set[str] = set()

    def add(ids, prio):
        for rid in ids:
            if rid not in seen:
                seen.add(rid)
                order.append((rid, prio))

    add(susp.loc[(susp["level"] == "L1") & (susp["gt"] != ""), "review_id"], 1)
    add(susp.loc[(susp["level"] == "L2") & (susp["pattern"] == "consensus_alt") & (susp["err_type"] == "WV"),
                 "review_id"], 2)
    rng = random.Random(0)
    for _, g in susp.groupby(CLUSTER_KEY, sort=True):
        if len(g) <= 10:
            add(g["review_id"], 3)
        else:
            l1, l2 = list(g.loc[g["level"] == "L1", "review_id"]), list(g.loc[g["level"] == "L2", "review_id"])
            add(rng.sample(l1, min(10, len(l1))) + rng.sample(l2, min(5, len(l2))), 3)
    add(v.loc[v["err_type"] == "FF_mask"].sort_values(["doc_id", "field"])["review_id"], 4)
    prob = set(docs.loc[docs["doc_problem"] == True, "doc_id"])  # noqa: E712
    add(v.loc[v["doc_id"].isin(prob)].sort_values(["doc_id", "field"])["review_id"], 4)

    crng = random.Random(0)
    l0 = sorted(set(v.loc[(v["level"] == "L0") & (v["n_wrong_raw"] == 0), "review_id"]) - seen)
    l1_free = sorted(set(v.loc[v["level"] == "L1", "review_id"]) - seen)
    controls = [(r, "L0_all_correct") for r in crng.sample(l0, min(15, len(l0)))]
    controls += [(r, "L1") for r in crng.sample(l1_free, min(10, len(l1_free)))]
    for rid, _ in controls:
        pos = crng.randint(0, len(order))
        prio = order[pos - 1][1] if pos > 0 else (order[0][1] if order else 5)
        order.insert(pos, (rid, prio))

    idx = v.set_index("review_id")
    rows = []
    for i, (rid, prio) in enumerate(order):
        r = idx.loc[rid]
        rows.append({"review_id": rid, "priority": prio, "batch": i // BATCH + 1, "doc_id": r["doc_id"],
                     "field": r["field"], "field_human": field_human.get(r["field"], r["field"]),
                     "doc_type": r["doc_type"], "gt": r["gt"], "printed": r["printed"],
                     "consensus_example": r["consensus_example"],
                     **{f"pred_{m}": r[f"pred_{m}"] for m in models}, "hint": r["hint"],
                     "page_paths": r["page_paths"], "prior_verdict": verdicts.get(rid, {}).get("verdict", "")})
    q = pd.DataFrame(rows)
    ctrl = pd.DataFrame(controls, columns=["review_id", "control"])
    if len(ctrl):
        ctrl["batch"] = ctrl["review_id"].map(dict(zip(q["review_id"], q["batch"])))
    return q, ctrl


# ----------------------------------------------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------------------------------------------
def md(df: pd.DataFrame, index: bool = False) -> str:
    if df is None or len(df) == 0:
        return "_(none)_"
    return df.to_markdown(index=index)


def level_hist(v: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col, name in (("level", "with abstentions (n_voting)"), ("level_raw", "abstention = wrong (raw)")):
        c = v[col].value_counts()
        rows.append({"variant": name, **{lv: int(c.get(lv, 0)) for lv in LEVELS}, "total": int(c.sum())})
    return pd.DataFrame(rows)


def sanity_checks(v: pd.DataFrame, models: list[str], frames: dict, out: Path, written: list[Path],
                  reproduce_mismatches: dict | None = None) -> list[tuple]:
    checks = []
    n = len(v)
    lc = v["level"].value_counts()
    checks.append(("level counts sum to n keys", int(lc.sum()) == n, f"{dict(lc)} sum={int(lc.sum())} n={n}"))
    l1 = v[v["level"] == "L1"]
    viol = 0
    for m in models:
        abst = set(frames[m].loc[frames[m]["json_valid"].eq("False"), "doc_id"])
        voting = ~l1["doc_id"].isin(abst)
        viol += int((voting & ~l1[f"outcome_{m}"].isin(WRONG)).sum())
    checks.append(("every L1 voting outcome in {WV,FN,FF}", viol == 0, f"violations={viol}"))
    tot_wrong = sum(int(frames[m]["outcome"].isin(WRONG).sum()) for m in models)
    s_raw = int(v["n_wrong_raw"].sum())
    checks.append(("sum models (WV+FN+FF) == sum n_wrong_raw", tot_wrong == s_raw,
                   f"WV+FN+FF={tot_wrong} sum n_wrong_raw={s_raw}"))
    susp = v[v["level"].isin(["L1", "L2"])]
    checks.append(("pattern counts sum to L1+L2", int(susp["pattern"].isin(PATTERNS).sum()) == len(susp),
                   f"{dict(Counter(susp['pattern']))} vs {len(susp)}"))
    checks.append(("hint counts sum to L1+L2", int(susp["hint"].isin(HINTS).sum()) == len(susp),
                   f"{dict(Counter(susp['hint']))} vs {len(susp)}"))
    paths = {p for pp in v["page_paths"].drop_duplicates() for p in pp.split(";") if p}
    missing = sorted(p for p in paths if not Path(p).exists())
    checks.append(("every page_path exists", not missing and bool(paths), f"{len(paths)} pages, missing={missing[:3]}"))
    if reproduce_mismatches is None:
        reproduce_mismatches = {m: sum(S.outcome(fld, gt or None, decode_pred(pred)).outcome != o for fld, gt, pred, o
                                       in zip(frames[m]["field"], frames[m]["gt"], frames[m]["pred"],
                                              frames[m]["outcome"])) for m in models}
    rec_mismatch = sum(reproduce_mismatches.values())
    checks.append(("current scorer + answers.json reproduce fields.csv outcomes (fails on a fields.csv scored by an "
                   "older scorer, e.g. round-1 runs/*/fields.csv)", rec_mismatch == 0,
                   f"mismatches={rec_mismatch} {reproduce_mismatches if rec_mismatch else ''}".strip()))
    outr = out.resolve()
    outside = [str(p) for p in written if outr not in p.resolve().parents and p.resolve() != outr]
    checks.append(("nothing written outside the output dir", not outside, f"files={len(written)} outside={outside}"))
    return checks


def write_report(path: Path, ctx: dict) -> None:
    v, susp, models = ctx["votes"], ctx["suspects"], ctx["models"]
    P = []
    P.append("# GT / input check — round 1\n")
    P.append("Generated by `uv run python -m harness.gt_check` (spec: PLAN.md). Hints order the review queue; they "
             "are not verdicts.\n")
    P.append("## Inputs\n")
    P.append(f"Protocol: `{ctx['protocol']}`\n")
    P.append(md(pd.DataFrame([{k: i[k] for k in ("run_id", "hf_model", "revision", "fields_path", "fields_sha256",
                                                 "rows", "error_rows")} for i in ctx["runs"]])))
    if ctx.get("gt_edits_tolerated"):
        P.append(f"\nGT edits after round 1 (reports/gt_check/applied_fixes.csv) where the input still holds the old "
                 f"answer: {ctx['gt_edits_tolerated']} keys (tolerated).\n")
    P.append("\n## Reconciliation with summary.md (\"## All\" per doc_type)\n")
    P.append(md(ctx["recon"]))
    P.append("\n## Levels\n")
    P.append(md(level_hist(v)))
    P.append("\nAbstaining (json_valid=False) docs: " + (", ".join(
        f"{d} ({m})" for d, m in ctx["abstain_docs"]) or "none") + "\n")
    P.append("\nModels wrong per key, n_wrong_raw histogram: " + json.dumps(
        {int(k): int(c) for k, c in sorted(Counter(v["n_wrong_raw"]).items())}) + "\n")
    P.append("\n### Level x err_type\n")
    P.append(md(pd.crosstab(v["level"], v["err_type"].replace("", "(none)")).reindex(LEVELS).fillna(0).astype(int),
                index=True))
    P.append("\n### Level x hint\n")
    P.append(md(pd.crosstab(v["level"], v["hint"].replace("", "(none)")).reindex(LEVELS).fillna(0).astype(int),
                index=True))
    P.append("\n### Suspects (L1+L2) by pattern\n")
    P.append(md(susp["pattern"].value_counts().rename_axis("pattern").reset_index()))

    P.append("\n## Top 20 clusters (source, field, err_type, hint)\n")
    cl = ctx["clusters"]
    P.append(md(cl.head(20)[CLUSTER_KEY + ["count", "n_L1", "sibling_field_mode"]]))
    idx = v.set_index("review_id")
    for _, c in cl.head(20).iterrows():
        P.append(f"\n**{c['source']} / {c['field']} / {c['err_type']} / {c['hint']}** — {c['count']} keys, "
                 f"{c['n_L1']} L1\n")
        ex = []
        for rid in (c["example_1"], c["example_2"]):
            if not rid:
                continue
            r = idx.loc[rid]
            first_page = r["page_paths"].split(";")[0] if r["page_paths"] else ""
            ex.append({"review_id": rid, "gt": r["gt"], "printed": r["printed"],
                       **{m: r[f"pred_{m}"] for m in models}, "consensus": r["consensus_example"],
                       "page": f"[page]({Path(first_page).as_uri()})" if first_page else ""})
        P.append(md(pd.DataFrame(ex)))

    P.append("\n## Source x field, top 30 by lift (n_suspect >= 2)\n")
    sf = ctx["groups"]["by_source_field"]
    sf2 = sf[sf["n_suspect"] >= 2].sort_values(["lift", "n_suspect", "source", "field"],
                                               ascending=[False, False, True, True], kind="mergesort")
    P.append(md(sf2.head(30)[["source", "field", "n_keys", "n_L1", "n_L2", "suspect_rate", "base_err_rate", "lift"]
                             + [f"hint_{h}" for h in HINTS]]))
    for name in ("by_field", "by_source", "by_lang", "by_doc_type", "by_variant", "by_kind", "by_field_masked",
                 "by_template"):
        g = ctx["groups"][name]
        cols = [c for c in g.columns if not c.startswith("hint_") and not c.startswith("pattern_")]
        P.append(f"\n### {name}\n")
        P.append(md(g[cols] if len(g) else g))

    P.append("\n## Candidates\n")
    P.append("\n### Document problems (docs.csv `doc_problem`)\n")
    d = ctx["docs"]
    P.append(md(d[d["doc_problem"] == True][["doc_id", "source", "variant", "n_fields", "n_suspect",  # noqa: E712
                                             "suspect_share", "hints", "twin_clean_ok"]]))
    P.append("\n### Prompt / definition problems\n")
    P.append("Rule: field suspect in >= 3 sources with lift >= 2, or a source x field cluster with >= 10 suspects of "
             "the same hint.\n")
    multi = (sf[(sf["lift"] >= 2) & (sf["n_suspect"] > 0)].groupby("field")["source"]
             .agg(lambda s: ";".join(sorted(s))).reset_index())
    multi["n_sources"] = multi["source"].str.count(";") + 1
    multi = multi[multi["n_sources"] >= 3].rename(columns={"source": "sources"})
    P.append(md(multi))
    big = (susp.groupby(["source", "field", "hint"]).size().rename("count").reset_index()
           .query("count >= 10").sort_values(["count", "source", "field"], ascending=[False, True, True]))
    P.append("\n")
    P.append(md(big))
    P.append("\n### Too-strict scorer (hint scorer_strict)\n")
    ss = susp[susp["hint"] == "scorer_strict"]
    ssg = (ss.groupby(["source", "field"]).agg(count=("review_id", "size"), id_prefix_only=("id_prefix_only", "sum"),
                                               gt_in_pred=("gt_in_pred", "sum"), pred_in_gt=("pred_in_gt", "sum"),
                                               example=("review_id", "first"))
           .reset_index().sort_values(["count", "source", "field"], ascending=[False, True, True]))
    P.append(md(ssg))
    P.append("\n### GT error candidates (isolated consensus_alt in otherwise clean source x field)\n")
    P.append("Rule: suspect with pattern consensus_alt whose source x field has <= 2 suspects and whose source has a "
             "suspect rate <= the overall rate.\n")
    src_rate = ctx["groups"]["by_source"].set_index("source")["suspect_rate"]
    overall = v["level"].isin(["L1", "L2"]).mean()
    sfn = sf.set_index(["source", "field"])["n_suspect"]
    iso = susp[(susp["pattern"] == "consensus_alt")
               & pd.Series([sfn.get((s, f), 0) <= 2 for s, f in zip(susp["source"], susp["field"])],
                           index=susp.index, dtype=bool)
               & susp["source"].map(src_rate).le(overall)]
    P.append(md(iso[["review_id", "level", "err_type", "hint", "gt", "consensus_example", "n_agree"]]))

    P.append("\n## Review\n")
    P.append(f"Queue: `review/queue.csv` ({ctx['queue_len']} items, batches of {BATCH}); verdicts are appended to "
             "`review/verdicts.jsonl` (PLAN section 6). Controls are listed only in `review/controls_key.csv`.\n")
    if ctx["verdicts"]:
        P.append(f"\n{len(ctx['verdicts'])} verdicts read ({ctx['bad_verdict_lines']} unreadable lines).\n")
        sv = susp["verdict_source"].value_counts() if "verdict_source" in susp else {}
        P.append(f"Suspects (L1+L2): {len(susp)}; with a verdict carried over from an earlier check "
                 f"{int(sv.get('carried', 0))}, with a verdict of this check {int(sv.get('own', 0))}, "
                 f"not yet reviewed {int((susp['verdict'] == '').sum())}.\n")
        vs = susp[susp["verdict"] != ""]
        if len(vs):
            P.append("\n### Verdict by cluster\n")
            P.append(md(pd.crosstab([vs[c] for c in CLUSTER_KEY], vs["verdict"]).reset_index()))
        ctrl = ctx["controls"]
        if len(ctrl):
            cv = ctrl.assign(verdict=ctrl["review_id"].map(lambda r: ctx["verdicts"].get(r, {}).get("verdict", "")))
            cv = cv[cv["verdict"] != ""]
            if len(cv):
                P.append("\n### Controls\n")
                P.append(md(pd.crosstab(cv["control"], cv["verdict"]).reset_index()))
        P.append("\nProposed fixes for the owner: `review/proposed_fixes.csv` (final/ is never edited).\n")
    else:
        P.append("\nNo verdicts yet.\n")

    P.append("\n## Sanity checks\n")
    P.append(md(pd.DataFrame(ctx["checks"], columns=["check", "ok", "detail"])))
    path.write_text("\n".join(P) + "\n")


# ----------------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------------
class Writer:
    def __init__(self, out: Path):
        self.out, self.written = out, []

    def path(self, rel: str) -> Path:
        p = self.out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        self.written.append(p)
        return p

    def csv(self, rel: str, df: pd.DataFrame) -> None:
        df.to_csv(self.path(rel), index=False)


def run(root: Path, protocol: Path, out: Path, carry_verdicts: list[Path] | None = None, **expect) -> int:
    """Full check; `expect` (n_runs, n_docs, n_rows, n_docs_fields) overrides the round-1 sizes; fields_root /
    fields_name choose the scored input (load); carry_verdicts: earlier verdict files (merge_verdicts)."""
    out.mkdir(parents=True, exist_ok=True)
    W = Writer(out)
    try:
        data = load(root, protocol, **expect)
    except CheckError as e:
        print(f"INPUT CHECK FAILED: {e}", file=sys.stderr)
        return 2
    recon = data["recon"]
    if not recon["ok"].all():
        W.path("report.md").write_text("# GT / input check — ABORTED\n\nReconciliation with summary.md failed.\n\n"
                                       + md(recon) + "\n")
        print("INPUT CHECK FAILED: reconciliation with summary.md, see report.md", file=sys.stderr)
        return 2
    models = data["models"]
    v = analyze(data["wide"], models)
    v = v[vote_columns(models)]
    groups = group_tables(v)
    docs = docs_table(v)

    review = out / "review"
    review.mkdir(parents=True, exist_ok=True)
    vpath = review / "verdicts.jsonl"
    if not vpath.exists():
        W.path("review/verdicts.jsonl").write_text("")
    verdicts, bad = merge_verdicts(list(carry_verdicts or []), vpath)

    susp = sort_suspects(v[v["level"].isin(["L1", "L2"])].copy())
    susp["verdict"] = susp["review_id"].map(lambda r: verdicts.get(r, {}).get("verdict", ""))
    susp["verdict_source"] = susp["review_id"].map(
        lambda r: "" if r not in verdicts else ("own" if verdicts[r]["_source"] == str(vpath) else "carried"))
    clusters = clusters_table(susp)
    fh = yaml.safe_load((root / "protocol" / "fields.yaml").read_text())["fields"]
    queue, controls = build_queue(v, susp, docs, models, fh, verdicts)

    W.csv("votes.csv", v)
    W.csv("suspects.csv", susp)
    for name in ("by_field", "by_source_field", "by_source", "by_lang", "by_doc_type", "by_variant", "by_kind",
                 "by_template", "by_lang_field_edb"):
        W.csv(f"{name}.csv", groups[name])
    W.csv("docs.csv", docs)
    W.csv("clusters.csv", clusters)
    W.csv("review/queue.csv", queue)
    W.csv("review/controls_key.csv", controls)
    if verdicts:
        idx = v.set_index("review_id")
        fixes = []
        for rid, rec in sorted(verdicts.items()):
            if rec.get("verdict") not in FIX_VERDICTS or rid not in idx.index:
                continue
            r = idx.loc[rid]
            fixes.append({"review_id": rid, "doc_id": r["doc_id"], "field": r["field"], "current_answer": r["gt"],
                          "current_printed": r["printed"], "verdict": rec.get("verdict"),
                          "proposed_answer": "" if rec.get("verdict") == "gt_value_absent"
                          else display(rec.get("correct_value")),
                          "confidence": rec.get("confidence", ""), "evidence": rec.get("evidence", ""),
                          "reviewer": rec.get("reviewer", ""), "ts": rec.get("ts", "")})
        W.csv("review/proposed_fixes.csv", pd.DataFrame(fixes, columns=[
            "review_id", "doc_id", "field", "current_answer", "current_printed", "verdict", "proposed_answer",
            "confidence", "evidence", "reviewer", "ts"]))

    abstain = sorted({(d, m) for m in models for d in
                      data["frames"][m].loc[data["frames"][m]["json_valid"].eq("False"), "doc_id"]})
    rpath = W.path("report.md")
    checks = sanity_checks(v, models, data["frames"], out, W.written, data["reproduce_mismatches"])
    ctx = {"votes": v, "suspects": susp, "models": models, "runs": data["runs"], "recon": recon,
           "gt_edits_tolerated": data["gt_edits_tolerated"],
           "protocol": str(protocol), "abstain_docs": abstain, "clusters": clusters, "groups": groups, "docs": docs,
           "queue_len": len(queue), "verdicts": verdicts, "bad_verdict_lines": bad, "controls": controls,
           "checks": checks}
    write_report(rpath, ctx)
    lc = v["level"].value_counts()
    print(f"keys={len(v)} L1={lc.get('L1', 0)} L2={lc.get('L2', 0)} queue={len(queue)} -> {out}")
    failed = [c for c in checks if not c[1]]
    for c in failed:
        print(f"SANITY CHECK FAILED: {c[0]}: {c[2]}", file=sys.stderr)
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--runs-from", default="protocol/round1.json")
    ap.add_argument("--out", default="reports/gt_check")
    ap.add_argument("--fields-root", default="runs", help="read <fields-root>/<run_id>/<fields-name> (+ summary.md)")
    ap.add_argument("--fields-name", default="fields.csv")
    ap.add_argument("--n-rows", type=int, help=f"expected rows per run (default {N_ROWS} for runs/, else the number "
                                               "of fields in final/ answers.json)")
    ap.add_argument("--n-docs", type=int, default=N_DOCS,
                    help=f"documents each run selected, config.json n_selected (default {N_DOCS}, round 1; "
                         "1572 for r1b on final v5)")
    ap.add_argument("--carry-verdicts", nargs="*", default=list(CARRY_DEFAULT),
                    help="verdict files of earlier checks, carried over by review_id (later files win; the --out "
                         "directory's own verdicts.jsonl wins over all)")
    a = ap.parse_args(argv)
    proto, out, froot = (Path(x) if Path(x).is_absolute() else ROOT / x for x in (a.runs_from, a.out, a.fields_root))
    rescore = froot != ROOT / "runs"
    n_rows = a.n_rows if a.n_rows is not None else (None if rescore else N_ROWS)
    # a re-score holds only the documents still in final/manifest.csv
    n_docs_fields = len(pd.read_csv(ROOT / "final" / "manifest.csv", dtype=str)) if rescore else None
    carry = [Path(x) if Path(x).is_absolute() else ROOT / x for x in a.carry_verdicts]
    return run(ROOT, proto, out, carry_verdicts=carry, n_rows=n_rows, fields_root=froot, fields_name=a.fields_name,
               n_docs=a.n_docs, n_docs_fields=n_docs_fields)


if __name__ == "__main__":
    sys.exit(main())
