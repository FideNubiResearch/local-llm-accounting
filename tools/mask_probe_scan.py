"""Closeout 1.2: find mask probes whose painted-over amount can still be derived from printed numbers.

  uv run python tools/mask_probe_scan.py [--out reports/gt_check/stage1/mask_probe_candidates.csv]

A mask probe is the painted field of a `__mask` document (manifest `masked_field`; answers.json `masked: true`,
answer null). For every amount probe (total, subtotal, tax_amount, total_gross, total_net, total_tax) the page is
read with Apple Vision OCR (tools/ocr_vision.swift, compiled into a temporary directory; no network) and the
value V of the same field in the base document is searched among the printed numbers:
  leak     V itself is printed;
  rounded  a number within 1 of V with at most one decimal (a rounded or pre-rounding total);
  sum2/3   V = a + b (+ c) of printed numbers (SUB_TOTAL + TAX, subtotal + service + tax, GST-summary parts);
  diff2/3  V = a - b (- c) (total - subtotal = tax; total - subtotal - service; amount - discount; cash - change);
  run      V = sum of 3 or more consecutive printed numbers (item lines).
Each number is read with normalize.amount_candidates ("36.000" is 36000 or 36). A hit is a candidate only: each is
verified on the page image before the probe is excluded (tools/apply_gt_review.py, MASK_PROBES, with evidence).
Read-only over final/; writes only --out.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import re
import subprocess
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness import normalize as N  # noqa: E402

AMOUNTS = {"total", "subtotal", "tax_amount", "total_gross", "total_net", "total_tax"}
EPS = Decimal("0.005")
NUM = re.compile(r"-?(?:\d[\d.,' ]*\d|\d|\.\d+)")


def ocr(pages: list[Path]) -> dict[str, list[str]]:
    with tempfile.TemporaryDirectory() as td:
        exe = Path(td) / "ocr_vision"
        subprocess.run(["swiftc", "-O", str(ROOT / "tools" / "ocr_vision.swift"), "-o", str(exe)], check=True)
        out = subprocess.run([str(exe), *map(str, pages)], check=True, capture_output=True, text=True).stdout
    res, cur = {}, None
    for ln in out.splitlines():
        if ln.startswith("=== "):
            cur = ln[4:]
            res[cur] = []
        elif cur is not None:
            res[cur].append(ln.split("\t", 1)[-1])
    return res


def numbers(lines: list[str]) -> list[tuple[Decimal, str]]:
    """Printed numbers in reading order: (value, source line); an ambiguous number gives every reading."""
    out = []
    for t in lines:
        for m in NUM.finditer(t):
            for a in sorted(N.amount_candidates(m.group().strip())):
                if a:
                    out.append((abs(a), t))
    return out


def derive(v: Decimal, nums: list[tuple[Decimal, str]]) -> list[str]:
    hits = []
    for a, t in nums:
        if abs(a - v) < EPS:
            hits.append(f"leak: '{t}'")
        elif abs(a - v) < 1 and (a * 10) == (a * 10).to_integral():
            hits.append(f"rounded {a}: '{t}'")
    uniq = list({a: t for a, t in nums}.items())
    for (a, ta), (b, tb) in itertools.permutations(uniq, 2):
        if a >= b and abs(a + b - v) < EPS:
            hits.append(f"sum2 {a}+{b}: '{ta}' | '{tb}'")
        if abs(a - b - v) < EPS:
            hits.append(f"diff2 {a}-{b}: '{ta}' | '{tb}'")
    if len(uniq) <= 60:
        for (a, ta), (b, tb), (c, tc) in itertools.permutations(uniq, 3):
            if a >= b >= c and abs(a + b + c - v) < EPS:
                hits.append(f"sum3 {a}+{b}+{c}: '{ta}' | '{tb}' | '{tc}'")
            if b >= c and abs(a - b - c - v) < EPS:
                hits.append(f"diff3 {a}-{b}-{c}: '{ta}' | '{tb}' | '{tc}'")
    seq = [a for a, _ in nums]
    for i in range(len(seq)):
        acc = Decimal(0)
        for j in range(i, min(len(seq), i + 30)):
            acc += seq[j]
            if j - i >= 2 and abs(acc - v) < EPS:
                hits.append(f"run {'+'.join(str(x) for x in seq[i:j + 1])}")
    return list(dict.fromkeys(hits))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="reports/gt_check/stage1/mask_probe_candidates.csv")
    a = ap.parse_args(argv)
    man = list(csv.DictReader(open(ROOT / "final" / "manifest.csv", newline="")))
    probes = []
    for r in man:
        f = r["masked_field"]
        if f not in AMOUNTS:
            continue
        ans = json.loads((ROOT / "final" / "docs" / r["doc_id"] / "answers.json").read_text())
        base = json.loads((ROOT / "final" / "docs" / r["base_doc"] / "answers.json").read_text())
        v = base["fields"].get(f, {}).get("answer")
        pages = [ROOT / "final" / "docs" / r["doc_id"] / p for p in ans["pages"]]
        probes.append((r["doc_id"], f, f in ans["fields"], v, pages))
    text = ocr([p for *_, pages in probes for p in pages])
    rows = []
    for doc, f, scored, v, pages in probes:
        hits = derive(Decimal(v), numbers([t for p in pages for t in text.get(str(p), [])])) if v else []
        rows.append({"doc_id": doc, "field": f, "base_value": v or "", "still_scored": scored,
                     "candidate": bool(hits), "n_hits": len(hits), "hits": " ; ".join(hits[:12])})
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{'CAND' if r['candidate'] else '    '} {r['doc_id']}::{r['field']} V={r['base_value']} "
              f"hits={r['n_hits']} {r['hits'][:160]}")
    print(f"{sum(r['candidate'] for r in rows)} candidates of {len(rows)} amount probes -> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
