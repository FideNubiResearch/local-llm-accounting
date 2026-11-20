"""Energy per document with powermetrics (needs `sudo -n /usr/bin/powermetrics`, see journal 2026-11-20).

  uv run python -m harness.energy [--docs protocol/samples/smoke.txt] [--idle 60] [--out reports/energy]

For each configuration: the 33 smoke documents are run with the same arguments as in the study (runs/e__<name>), while
powermetrics samples CPU+GPU+ANE power every second. Energy of a run = sum of samples inside [model loaded, last document]
(power in mW x seconds); idle power is measured before the first run and subtracted for the "above idle" column.
Documents of the energy runs are the smoke sample only; their answers are not scored here.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

from harness.study import ROOT, args_for

CONFIGS = [("round_final", "f__gemma4-12b__q6"), ("round_final", "f__qwen3.5-4b__q6"),
           ("round2_extractors", "r2__nuextract3-4b__q6"), ("round2_extractors", "r2__lift-9b__q6c")]
CMD = ["sudo", "-n", "/usr/bin/powermetrics", "--samplers", "cpu_power,gpu_power,ane_power", "-i", "1000"]


class Meter:
    def __init__(self):
        self.samples: list[tuple[float, float, float, float, float]] = []   # t, cpu, gpu, ane, combined (mW)
        self.p = subprocess.Popen(CMD, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        self.t = threading.Thread(target=self._read, daemon=True)
        self.t.start()

    def _read(self):
        try:
            self._loop()
        except ValueError:                 # stdout closed by stop()
            pass

    def _loop(self):
        cur: dict[str, float] = {}
        for line in self.p.stdout:
            m = re.match(r"(CPU|GPU|ANE) Power: (\d+) mW", line)
            if m and m.group(1) not in cur:
                cur[m.group(1)] = float(m.group(2))
            m = re.match(r"Combined Power \(CPU \+ GPU \+ ANE\): (\d+) mW", line)
            if m:
                self.samples.append((time.time(), cur.get("CPU", 0), cur.get("GPU", 0), cur.get("ANE", 0), float(m.group(1))))
                cur = {}

    def window(self, a: float, b: float) -> list[tuple]:
        return [s for s in self.samples if a <= s[0] <= b]

    def stop(self):
        try:
            self.p.stdout.close()          # powermetrics ends on its next write (SIGPIPE)
        except Exception:
            pass
        try:
            self.p.wait(timeout=10)
        except Exception:
            pass


def mean(rows, i):
    return sum(r[i] for r in rows) / len(rows) if rows else float("nan")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="protocol/samples/smoke.txt")
    ap.add_argument("--idle", type=int, default=60)
    ap.add_argument("--out", default="reports/energy")
    a = ap.parse_args(argv)
    meter = Meter()
    time.sleep(5)
    t0 = time.time()
    time.sleep(a.idle)
    idle = meter.window(t0, time.time())
    if not idle:
        meter.stop()
        sys.exit("no powermetrics samples (is `sudo -n powermetrics` allowed?)")
    idle_mw = mean(idle, 4)
    print(f"idle: {idle_mw:.0f} mW over {len(idle)} s", flush=True)
    rows = []
    for qf, rid in CONFIGS:
        e = next(r for r in json.loads((ROOT / "protocol" / f"{qf}.json").read_text())["runs"] if r["run_id"] == rid)
        e = {**e, "run_id": "e__" + rid.split("__", 1)[1], "docs": a.docs}
        study = {"prompt": e.get("prompt", "P1b"), "where": []}
        cmd = [sys.executable, "-m", "harness.run", *args_for(study, e)]
        t_start = time.time()
        r = subprocess.run(cmd, cwd=ROOT)
        t_end = time.time()
        cfg = json.loads((ROOT / "runs" / e["run_id"] / "config.json").read_text())
        preds = [json.loads(l) for l in (ROOT / "runs" / e["run_id"] / "predictions.jsonl").read_text().splitlines() if l.strip()]
        work_s = sum(p["wall_s"] for p in preds)
        win = meter.window(t_end - work_s - (len(preds) * 0.5), t_end)      # generation phase (load excluded)
        mj = sum(s[4] for s in win)                                          # mW x 1 s samples = mJ
        net = sum(s[4] - idle_mw for s in win)
        rows.append({"run": e["run_id"], "exit": r.returncode, "docs": len(preds), "errors": sum(1 for p in preds if p["error"]),
                     "work_s": round(work_s, 1), "samples": len(win), "cpu_mw": round(mean(win, 1)), "gpu_mw": round(mean(win, 2)),
                     "ane_mw": round(mean(win, 3)), "total_mw": round(mean(win, 4)),
                     "wh_per_doc": round(mj / 3.6e6 / max(len(preds), 1), 4), "wh_per_doc_above_idle": round(net / 3.6e6 / max(len(preds), 1), 4),
                     "s_per_doc": round(work_s / max(len(preds), 1), 1), "peak_gb": max((p["peak_gb"] for p in preds), default=0)})
        print(rows[-1], flush=True)
        time.sleep(30)                                                       # cool down between configurations
    meter.stop()
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    L = ["# Энергия на документ (powermetrics)", "",
         f"Выборка: {a.docs} (33 документа), CPU+GPU+ANE, шаг 1 с. Простой машины: {idle_mw / 1000:.2f} Вт ({len(idle)} с). "
         "Учтена фаза обработки документов (загрузка модели исключена). Мощность всей системы (розетка) не измерялась.", "",
         "| Конфигурация | Док. | Ошибок | с/док | CPU, Вт | GPU, Вт | Всего, Вт | Вт·ч/док | Вт·ч/док сверх простоя | Пик, ГБ |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['run']} | {r['docs']} | {r['errors']} | {r['s_per_doc']} | {r['cpu_mw'] / 1000:.1f} | {r['gpu_mw'] / 1000:.1f} | "
                 f"{r['total_mw'] / 1000:.1f} | {r['wh_per_doc']} | {r['wh_per_doc_above_idle']} | {r['peak_gb']} |")
    (out / "energy.md").write_text("\n".join(L) + "\n")
    (out / "energy.json").write_text(json.dumps({"idle_mw": idle_mw, "rows": rows}, indent=1))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
