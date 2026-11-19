"""GT arithmetic check (closeout stage 2.2): do the ground-truth values of a document agree with each other?

  uv run python -m harness.gt_arith [--out reports/gt_check/stage2/arith.csv] [--no-ocr]

Checks per document (the GT answer of each field; a check runs only when all its fields have a value):
  inv_sum            invoice  total_net + total_tax = total_gross
  inv_net_le_gross   invoice  |total_net| <= |total_gross|
  inv_tax_le_gross   invoice  |total_tax| <= |total_gross|
  rcpt_sum           receipt  subtotal + tax_amount = total
  rcpt_subtotal_le_total  receipt  |subtotal| <= |total|
  rcpt_tax_lt_total  receipt  |tax_amount| < |total|
  due_ge_issue       invoice  due_date >= issue_date (some reading of each date; dd/mm vs mm/dd counts)
  period_order       bank statement  period_end >= period_start
Tolerance: 0.01, or 1 unit for currencies without decimals (IDR, KRW, JPY; receipts have no currency field, so the
currency comes from the source: cord_v2 IDR, korie KRW). Amount comparisons use absolute values (credit notes).
Line items are not in the GT, so a line-item sum check is not possible.

Every violation is listed with severity (amounts: relative difference >= 5 % high, >= 0.5 % med, else low; dates:
more than a year apart high, else med) and a status: `explained` when a legitimate reason is likely, else
`unexplained` (these go to the stage-2 review queue). Explanations, first match:
  accepted_alternative  an accepted alternative answer (answers.json `accepted`) satisfies the rule;
  fatura_generator      FATURA: the generator prints random totals and dates that need not agree (final/README.md);
  rounding              |diff| <= 0.05 (decimal currencies) or < 100 (IDR/KRW/JPY);
  tax_inclusive         receipt subtotal == total and tax > 0: the subtotal is printed tax-inclusive;
  extra_line            |diff| itself is printed on the page (service charge, discount, rounding, shipping line);
                        read with Apple Vision OCR (tools/ocr_vision.swift; cached in ocr_cache.json next to --out;
                        --no-ocr skips it). A bare integer under 1000 does not count (quantities, VAT rates).
Read-only over final/; writes only --out, the summary next to it (arith_summary.csv) and the OCR cache.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import re
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

from harness import normalize as N

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "final"

ZERO_DEC = {"IDR", "KRW", "JPY"}
SOURCE_CURRENCY = {"cord_v2": "IDR", "korie": "KRW"}
CHECKS = ("inv_sum", "inv_net_le_gross", "inv_tax_le_gross", "rcpt_sum", "rcpt_subtotal_le_total",
          "rcpt_tax_lt_total", "due_ge_issue", "period_order")
# check -> doc_type, fields (for a sum: a + b = c; for le/lt: part, total; for dates: earlier, later)
SPEC = {
    "inv_sum": ("invoice", ("total_net", "total_tax", "total_gross")),
    "inv_net_le_gross": ("invoice", ("total_net", "total_gross")),
    "inv_tax_le_gross": ("invoice", ("total_tax", "total_gross")),
    "rcpt_sum": ("receipt", ("subtotal", "tax_amount", "total")),
    "rcpt_subtotal_le_total": ("receipt", ("subtotal", "total")),
    "rcpt_tax_lt_total": ("receipt", ("tax_amount", "total")),
    "due_ge_issue": ("invoice", ("issue_date", "due_date")),
    "period_order": ("bank_statement", ("period_start", "period_end")),
}
COLUMNS = ["doc_id", "source", "doc_type", "check", "fields", "values", "diff", "rel_diff", "currency", "tol",
           "severity", "status", "explanation", "evidence", "page_paths"]
NUM = re.compile(r"-?(?:\d[\d.,' ]*\d|\d|\.\d+)")


# ----------------------------------------------------------------------------------------------------------------
# pure helpers (tested in tests/test_gt_arith.py)
# ----------------------------------------------------------------------------------------------------------------
def tolerance(currency: str | None) -> Decimal:
    return Decimal(1) if (currency or "").upper() in ZERO_DEC else Decimal("0.01")


def doc_currency(source: str, fields: dict) -> str:
    c = (fields.get("currency") or {}).get("answer")
    return N.currency(c) if c else SOURCE_CURRENCY.get(source, "")


def values_of(field: dict | None) -> list:
    """GT answer first, then accepted alternatives (null answers give nothing)."""
    if not field or field.get("answer") is None:
        return []
    return [field["answer"]] + [a for a in field.get("accepted") or [] if a is not None]


def amount_holds(check: str, vals: tuple[Decimal, ...], tol: Decimal) -> bool:
    if check in ("inv_sum", "rcpt_sum"):
        a, b, c = vals
        return abs(a + b - c) <= tol
    part, total = (abs(x) for x in vals)
    if check == "rcpt_tax_lt_total":
        return part < total
    return part <= total + tol


def amount_diff(check: str, vals: tuple[Decimal, ...]) -> Decimal:
    """Sum checks: a + b - c; le/lt checks: |part| - |total|."""
    if check in ("inv_sum", "rcpt_sum"):
        a, b, c = vals
        return a + b - c
    return abs(vals[0]) - abs(vals[1])


def date_holds(earlier: set, later: set) -> bool:
    """Some reading of each date puts `later` on or after `earlier`."""
    return any(b >= a for a in earlier for b in later)


def severity_amount(diff: Decimal, base: Decimal) -> str:
    rel = abs(diff) / abs(base) if base else Decimal(1)
    return "high" if rel >= Decimal("0.05") else "med" if rel >= Decimal("0.005") else "low"


def printed_numbers(lines: list[str]) -> list[tuple[Decimal, str]]:
    """(absolute value, token) of the numbers on the page; a bare integer under 1000 is skipped (quantities, rates);
    an ambiguous token ("17.850") gives every reading."""
    out = []
    for t in lines:
        for m in NUM.finditer(t):
            tok = m.group().strip()
            bare = not re.search(r"[.,' ]\d", tok)
            for a in N.amount_candidates(tok):
                if a and not (bare and abs(a) < 1000):
                    out.append((abs(a), tok))
    return out


def find_printed(value: Decimal, nums: list[tuple[Decimal, str]]) -> str:
    for a, tok in nums:
        if abs(a - abs(value)) < Decimal("0.005"):
            return tok
    return ""


def explain(check: str, source: str, vals: tuple, alts_ok: bool, diff: Decimal | None, currency: str,
            nums: list[tuple[Decimal, str]] | None) -> tuple[str, str]:
    """(explanation, evidence) or ("", "")."""
    if alts_ok:
        return "accepted_alternative", "an accepted alternative answer satisfies the rule"
    if source == "fatura":
        return "fatura_generator", "FATURA generator totals / dates are random and need not agree"
    if diff is None:
        return "", ""
    zero = currency.upper() in ZERO_DEC
    if diff and abs(diff) <= (Decimal(99) if zero else Decimal("0.05")):
        return "rounding", f"|diff| {abs(diff)}"
    if check == "rcpt_sum":
        sub, tax, tot = vals
        if abs(sub) == abs(tot) and tax:
            return "tax_inclusive", "subtotal equals total: printed tax-inclusive"
    if nums is not None and abs(diff) not in {abs(x) for x in vals}:
        tok = find_printed(diff, nums)
        if tok:
            return "extra_line", f"difference {abs(diff)} printed on the page as '{tok}'"
    return "", ""


def check_doc(doc: dict, source: str, page_paths: str, ocr_lines: list[str] | None = None) -> list[dict]:
    """All violations of one document (answers.json dict)."""
    f = doc["fields"]
    cur = doc_currency(source, f)
    tol = tolerance(cur)
    nums = printed_numbers(ocr_lines) if ocr_lines is not None else None
    out = []
    for check in CHECKS:
        dtype, names = SPEC[check]
        if doc["doc_type"] != dtype or not all(values_of(f.get(n)) for n in names):
            continue
        raw = tuple(f[n]["answer"] for n in names)
        row = {"doc_id": doc["doc_id"], "source": source, "doc_type": dtype, "check": check,
               "fields": ";".join(names), "values": ";".join(f"{n}={v}" for n, v in zip(names, raw)),
               "currency": cur, "page_paths": page_paths}
        if check in ("due_ge_issue", "period_order"):
            ds = [N.dates(v) for v in raw]
            if not all(ds) or date_holds(*ds):
                continue
            alts = [[N.dates(v) for v in values_of(f[n])] for n in names]
            alts_ok = any(a and b and date_holds(a, b) for a, b in itertools.product(*alts))
            gap = (min(ds[0]) - max(ds[1])).days
            expl, ev = explain(check, source, raw, alts_ok, None, cur, nums)
            row.update(diff=f"{gap}d", rel_diff="", tol="0d", severity="high" if gap > 366 else "med")
        else:
            vals = tuple(N.amount(v) for v in raw)
            if None in vals or amount_holds(check, vals, tol):
                continue
            alts = [[N.amount(v) for v in values_of(f[n])] for n in names]
            alts_ok = any(None not in c and amount_holds(check, c, tol) for c in itertools.product(*alts))
            diff = amount_diff(check, vals)
            base = vals[-1]
            expl, ev = explain(check, source, vals, alts_ok, diff, cur, nums)
            rel = abs(diff) / abs(base) if base else Decimal(1)
            row.update(diff=str(diff), rel_diff=f"{rel:.4f}", tol=str(tol), severity=severity_amount(diff, base))
        row.update(status="explained" if expl else "unexplained", explanation=expl, evidence=ev)
        out.append(row)
    return out


def summary(rows: list[dict], checked: Counter) -> list[dict]:
    """Per source x check: n_checked, n_violations, n_explained, n_unexplained (plus an ALL row per check)."""
    c = Counter((r["source"], r["check"], r["status"]) for r in rows)
    keys = sorted(checked)
    out = []
    for src, chk in keys:
        e, u = c[(src, chk, "explained")], c[(src, chk, "unexplained")]
        out.append({"source": src, "check": chk, "n_checked": checked[(src, chk)], "n_violations": e + u,
                    "n_explained": e, "n_unexplained": u})
    for chk in CHECKS:
        rs = [r for r in out if r["check"] == chk]
        if rs:
            out.append({"source": "ALL", "check": chk, **{k: sum(r[k] for r in rs) for k in
                                                         ("n_checked", "n_violations", "n_explained",
                                                          "n_unexplained")}})
    return out


# ----------------------------------------------------------------------------------------------------------------
# I/O
# ----------------------------------------------------------------------------------------------------------------
def load_docs(final: Path = FINAL) -> list[tuple[dict, str, list[Path]]]:
    man = list(csv.DictReader(open(final / "manifest.csv", newline="")))
    out = []
    for r in man:
        d = final / "docs" / r["doc_id"]
        doc = json.loads((d / "answers.json").read_text())
        out.append((doc, r["source"], [d / p for p in doc["pages"]]))
    return out


def checked_counts(docs) -> Counter:
    c = Counter()
    for doc, src, _ in docs:
        for check in CHECKS:
            dtype, names = SPEC[check]
            if doc["doc_type"] == dtype and all(values_of(doc["fields"].get(n)) for n in names):
                c[(src, check)] += 1
    return c


def ocr_cached(pages: list[Path], cache_path: Path) -> dict[str, list[str]]:
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    keyed = {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): p for p in pages}
    todo = [p for k, p in keyed.items() if k not in cache]
    if todo:
        sys.path.insert(0, str(ROOT / "tools"))
        from mask_probe_scan import ocr  # noqa: E402  (Apple Vision, compiled on the fly)
        got = ocr(todo)
        for k, p in keyed.items():
            if k not in cache:
                cache[k] = got.get(str(p), [])
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=0, sort_keys=True))
    return {k: cache[k] for k in keyed}


def run(out: Path, use_ocr: bool = True, final: Path = FINAL) -> list[dict]:
    docs = load_docs(final)
    pp = {doc["doc_id"]: ";".join(str(p) for p in pages) for doc, _, pages in docs}
    rows = [r for doc, src, _ in docs for r in check_doc(doc, src, pp[doc["doc_id"]])]
    if use_ocr and rows:
        viol = {r["doc_id"] for r in rows}
        pages = [p for doc, _, ps in docs if doc["doc_id"] in viol for p in ps]
        text = ocr_cached(pages, out.parent / "ocr_cache.json")
        rows = []
        for doc, src, ps in docs:
            first = check_doc(doc, src, pp[doc["doc_id"]])
            if not first:
                continue
            lines = [t for p in ps for t in text.get(str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),
                                                     [])]
            rows += check_doc(doc, src, pp[doc["doc_id"]], lines)
    rows.sort(key=lambda r: (r["status"] != "unexplained", r["source"], r["doc_id"], CHECKS.index(r["check"])))
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    summ = summary(rows, checked_counts(docs))
    with open(out.parent / "arith_summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["source", "check", "n_checked", "n_violations", "n_explained",
                                           "n_unexplained"])
        w.writeheader()
        w.writerows(summ)
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="reports/gt_check/stage2/arith.csv")
    ap.add_argument("--no-ocr", action="store_true", help="skip the extra_line explanation (no page OCR)")
    a = ap.parse_args(argv)
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    rows = run(out, use_ocr=not a.no_ocr)
    c = Counter((r["source"], r["status"]) for r in rows)
    for (src, st), n in sorted(c.items()):
        print(f"{src:22s} {st:12s} {n}")
    print(f"{len(rows)} violations ({sum(r['status'] == 'unexplained' for r in rows)} unexplained) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
