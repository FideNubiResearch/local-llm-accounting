"""Machine load sampler (no sudo): CPU, memory, swap, memory pressure, GPU utilization and memory, thermal warnings.

Started by harness/study.py; appends one JSON line every 15 s to runs/system.jsonl. Energy needs powermetrics
(sudo) and is not sampled here.
"""
from __future__ import annotations

import json
import re
import subprocess
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs" / "system.jsonl"
PRESSURE = {1: "normal", 2: "warning", 4: "critical"}


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout
    except Exception:
        return ""


def sample() -> dict:
    import psutil

    vm, sw = psutil.virtual_memory(), psutil.swap_memory()
    g = 2 ** 30                                 # GB as macOS shows them (16 GB machine = 16)
    s = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "cpu_pct": psutil.cpu_percent(interval=None),
         "mem_used_gb": round((vm.total - vm.available) / g, 2), "mem_total_gb": round(vm.total / g, 2),
         "swap_gb": round(sw.used / g, 2)}
    lvl = _run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"]).strip()
    s["pressure"] = PRESSURE.get(int(lvl), lvl) if lvl.isdigit() else None
    io = _run(["ioreg", "-r", "-d", "1", "-c", "IOAccelerator"])
    m = re.search(r'"Device Utilization %"=(\d+)', io)
    s["gpu_pct"] = int(m.group(1)) if m else None
    m = re.search(r'"In use system memory"=(\d+)', io)
    s["gpu_mem_gb"] = round(int(m.group(1)) / 2 ** 30, 2) if m else None
    th = _run(["pmset", "-g", "therm"])
    s["thermal_warning"] = not ("No thermal warning" in th and "No performance warning" in th) if th else None
    return s


def loop(stop: threading.Event, every: int = 15):
    import psutil

    psutil.cpu_percent(interval=None)          # first call primes the counter
    while not stop.is_set():
        try:
            with open(OUT, "a") as f:
                f.write(json.dumps(sample()) + "\n")
        except Exception:
            pass
        stop.wait(every)
