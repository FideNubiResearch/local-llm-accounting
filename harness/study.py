"""Run a queue of runs (protocol/round*.json) one after another, keeping the dashboard fresh.

  caffeinate -i uv run python -m harness.study protocol/round1.json

- Runs go strictly in file order. Finished runs are skipped, an interrupted run continues where it stopped.
- An entry with "hold" waits: the file is re-read every minute, so removing "hold" (after setup is checked)
  lets the queue continue without a restart.
- After each run: runs/<run_id>/summary.md. The dashboard (runs/dashboard.html) is rebuilt every minute;
  machine load is sampled every 15 s into runs/system.jsonl (harness/monitor.py).
"""
from __future__ import annotations

import json
import sys
import threading
import time
import traceback
from pathlib import Path

from harness import dashboard, monitor, report, run

ROOT = Path(__file__).resolve().parents[1]


def finished(run_id: str) -> bool:
    cfg = ROOT / "runs" / run_id / "config.json"
    if not cfg.exists():
        return False
    c = json.loads(cfg.read_text())
    return bool(c.get("finished_at") or (cfg.parent / "ABORTED.json").exists())     # aborted by harness.memguard: recorded, not retried


def args_for(study: dict, e: dict) -> list[str]:
    a = ["--model", e["model"], "--revision", e["revision"], "--prompt", e.get("prompt", study["prompt"]),
         "--run-id", e["run_id"]]
    where = e.get("where", study.get("where"))
    if where:
        a += ["--where", *where]
    docs = e.get("docs", study.get("docs"))          # file with doc_ids (round-2 sample), relative to the project
    if docs:
        a += ["--docs", str(ROOT / docs)]
    for k in ("max_pixels", "max_soft_tokens", "max_tokens", "limit"):
        if e.get(k) is not None:
            a += [f"--{k.replace('_', '-')}", str(e[k])]
    if e.get("constrained"):
        a.append("--constrained")
    return a


def keep_dashboard_fresh(stop: threading.Event):
    while not stop.is_set():
        try:
            dashboard.build(60)
        except Exception:
            traceback.print_exc()
        stop.wait(60)


def main(path: str):
    stop = threading.Event()
    threading.Thread(target=keep_dashboard_fresh, args=(stop,), daemon=True).start()
    threading.Thread(target=monitor.loop, args=(stop,), daemon=True).start()
    try:
        i = 0
        while True:
            study = json.loads(Path(path).read_text())
            if i >= len(study["runs"]):
                break
            e = study["runs"][i]
            if finished(e["run_id"]):
                i += 1
                continue
            if e.get("hold"):
                print(f"{time.strftime('%H:%M')} waiting: {e['run_id']} - {e['hold']}", flush=True)
                time.sleep(60)
                continue
            try:
                run.main(args_for(study, e))
                report.main(str(ROOT / "runs" / e["run_id"]))
            except Exception:
                traceback.print_exc()          # recorded; a failed run stays unfinished and is retried on restart
                print(f"FAILED {e['run_id']}, moving on", flush=True)
            i += 1
        print("study done", flush=True)
    finally:
        stop.set()
        dashboard.build(None)


if __name__ == "__main__":
    main(sys.argv[1])
