"""Experiment dashboard: one local HTML page with the dataset composition and every run's scores.

  uv run python -m harness.dashboard            # writes runs/dashboard.html
  uv run python -m harness.dashboard --watch 60 # rebuild every 60 s while runs are going (page reloads itself)

Only aggregate numbers go into the page: no document images, no extracted values.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from pathlib import Path

import pandas as pd

from harness.report import FINAL, GENERATED, ROOT, field_rows, summarize

RUNS = ROOT / "runs"
OUT = RUNS / "dashboard.html"
TYPES = ["invoice", "receipt", "bank_statement"]


def dataset() -> dict:
    rows = list(csv.DictReader(open(FINAL / "manifest.csv")))
    uniq, real = defaultdict(set), defaultdict(set)
    for r in rows:
        base = r["base_doc"] or r["doc_id"].replace("__clean", "").replace("__photo", "")
        uniq[(r["lang"], r["doc_type"])].add(base)
        if r["source"] not in GENERATED:
            real[(r["lang"], r["doc_type"])].add(base)
    langs = sorted({l for l, _ in uniq}, key=lambda l: (l != "en", -sum(len(uniq[(l, t)]) for t in TYPES)))
    return {"docs": len(rows), "independent": sum(len(v) for v in uniq.values()),
            "values": sum(int(r["n_values"]) for r in rows), "nulls": sum(int(r["n_null"]) for r in rows),
            "langs": langs, "types": TYPES,
            "cells": {f"{l}|{t}": [len(uniq[(l, t)]), len(real[(l, t)])] for l in langs for t in TYPES}}


def runs() -> list[dict]:
    out = []
    for d in sorted(RUNS.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        cfg_p, pred_p = d / "config.json", d / "predictions.jsonl"
        if not (d.is_dir() and cfg_p.exists() and pred_p.exists() and pred_p.stat().st_size):
            continue
        cfg = json.loads(cfg_p.read_text())
        df = field_rows(d)
        tot = summarize(df.assign(all="all"), ["all"]).iloc[0].to_dict()
        cells = summarize(df, ["lang", "doc_type"]).to_dict("records")
        fields = summarize(df, ["doc_type", "field"]).to_dict("records")
        age = time.time() - pred_p.stat().st_mtime
        docs = df.drop_duplicates("doc_id")
        preds = [json.loads(l) for l in pred_p.read_text().splitlines() if l.strip()]
        # documents predicted at run time but excluded from final/ since then (e.g. closeout 1.1) are not "left to do"
        in_final = {r["doc_id"] for r in csv.DictReader(open(FINAL / "manifest.csv"))}
        n_dropped = len({p["doc_id"] for p in preds} - in_final)
        med = lambda k: (lambda v: round(float(pd.Series(v).median()), 1) if v else None)([p[k] for p in preds if p.get(k) is not None])
        tech = {"ttft_s": med("ttft_s"), "prompt_tokens": med("prompt_tokens"), "gen_tokens": med("gen_tokens"),
                "prompt_tps": med("prompt_tps"), "gen_tps": med("gen_tps"),
                "rss_gb": round(max(p["rss_gb"] for p in preds) * 1e9 / 2 ** 30, 2),
                "truncated": sum(p.get("finish") == "length" for p in preds)}
        series = [[p["wall_s"], p["peak_gb"] * 1e9 / 2 ** 30] for p in preds[-400:]]
        out.append({"id": d.name, "model": cfg["model"], "prompt": cfg["prompt"],
                    "constrained": cfg.get("constrained"),
                    "n_selected": cfg["n_selected"] - n_dropped if cfg.get("n_selected") else None,
                    "n_dropped": n_dropped,
                    "load_peak_gb": cfg.get("load_peak_gb"), "peak_gb": round(float(df["peak_gb"].max()) * 1e9 / 2 ** 30, 2),
                    "tech": tech, "series": series,
                    "errors": int(df.drop_duplicates("doc_id")["error"].notna().sum()),
                    "active": not cfg.get("finished_at") and age < 300,
                    "finished": bool(cfg.get("finished_at")), "updated": time.strftime("%Y-%m-%d %H:%M", time.localtime(pred_p.stat().st_mtime)),
                    "total": tot, "cells": cells, "fields": fields})
    return out


def studies(by_id: dict) -> list[dict]:
    """Queues from protocol/round*.json with the state of each entry."""
    from harness.run import manifest, select

    out = []
    for path in sorted((ROOT / "protocol").glob("round*.json")):
        st = json.loads(path.read_text())
        entries = []
        for e in st["runs"]:
            r = by_id.get(e["run_id"])
            n_total = (r or {}).get("n_selected") or len(select(manifest(), e.get("where", st.get("where", [])), None,
                                                                 e.get("limit")))
            done = r["total"]["docs"] if r else 0
            sec = (r["total"]["sec_median"] if r else None) or e.get("est_sec")
            state = ("done" if r and r["finished"] else "running" if r and r["active"] else
                     "hold" if e.get("hold") else "stopped" if r else "queued")
            entries.append({"run_id": e["run_id"], "model": e["model"], "state": state, "hold": e.get("hold"),
                            "done": done, "total": n_total, "sec": sec, "measured": bool(r),
                            "left_h": round((n_total - done) * (sec or 0) / 3600, 1)})
        out.append({"name": st["name"], "file": path.name, "entries": entries})
    return out


def machine(hours: float = 3) -> dict:
    """Last samples of runs/system.jsonl (harness/monitor.py)."""
    p = RUNS / "system.jsonl"
    if not p.exists():
        return {"samples": []}
    rows = [json.loads(l) for l in p.read_text().splitlines()[-int(hours * 3600 / 15):] if l.strip()]
    return {"samples": rows}


def clean(o):
    """NaN -> None so the page gets valid JSON."""
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [clean(v) for v in o]
    if isinstance(o, float) and o != o:
        return None
    return o


def build(refresh: int | None) -> None:
    rs = runs()
    data = clean({"built": time.strftime("%Y-%m-%d %H:%M:%S"), "dataset": dataset(), "runs": rs,
                  "studies": studies({r["id"]: r for r in rs}), "machine": machine()})
    html = (Path(__file__).with_name("dashboard.html").read_text()
            .replace("/*DATA*/null", json.dumps(data, ensure_ascii=False))
            .replace("<!--REFRESH-->", f'<meta http-equiv="refresh" content="{refresh}">' if refresh else ""))
    OUT.write_text(html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", type=int, metavar="SECONDS")
    a = ap.parse_args()
    while True:
        build(a.watch)
        print(f"{time.strftime('%H:%M:%S')} {OUT}", flush=True)
        if not a.watch:
            break
        time.sleep(a.watch)


if __name__ == "__main__":
    main()
