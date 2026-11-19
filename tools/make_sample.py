"""Round-2 sample of final/ (protocol/preregistration.md): every masked document, the rest stratified.

  uv run python tools/make_sample.py [--n 400] [--seed 0] [--out protocol/samples/round2.txt]

Strata = source x lang x doc_type x variant (masked documents excluded, they are all taken). Each stratum gets a
share proportional to its size (largest remainder), at least min(2, size). Deterministic for a given seed.
"""
from __future__ import annotations

import argparse
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def sample(m: pd.DataFrame, n: int, seed: int) -> list[str]:
    masked = m[m["masked_field"] != ""]
    rest = m[m["masked_field"] == ""]
    left = n - len(masked)
    groups = {k: sorted(g["doc_id"]) for k, g in rest.groupby(["source", "lang", "doc_type", "variant"])}
    base = {k: min(2, len(v)) for k, v in groups.items()}
    extra = left - sum(base.values())
    total = sum(len(v) - base[k] for k, v in groups.items())
    quota = {k: (len(v) - base[k]) * extra / total for k, v in groups.items()}
    take = {k: base[k] + int(quota[k]) for k in groups}
    for k in sorted(groups, key=lambda k: quota[k] - int(quota[k]), reverse=True)[: left - sum(take.values())]:
        take[k] += 1
    rng = random.Random(seed)
    out = sorted(masked["doc_id"])
    for k in sorted(groups):
        out += rng.sample(groups[k], min(take[k], len(groups[k])))
    return sorted(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="protocol/samples/round2.txt")
    a = ap.parse_args()
    m = pd.read_csv(ROOT / "final" / "manifest.csv", dtype=str, keep_default_na=False)
    ids = sample(m, a.n, a.seed)
    (ROOT / a.out).write_text("\n".join(ids) + "\n")
    s = m[m["doc_id"].isin(ids)]
    print(len(ids), "documents ->", a.out)
    print(s.groupby(["source", "doc_type"]).size().to_string())
    print(s["lang"].value_counts().to_dict(), s["variant"].value_counts().to_dict())


if __name__ == "__main__":
    main()
