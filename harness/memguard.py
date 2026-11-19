"""Memory guard for a single run on the 16 GB Mac mini.

Why: on 2026-11-15 gemma4-12b q8 pushed the machine into swap (1 -> 5 GB, pressure critical) and the kernel watchdog
rebooted it (panic 20:39:30). Prefill of an image is one blocking Metal call, so it cannot be interrupted from the
generation loop; a watcher thread ends the whole process instead.

Rule (protocol/preregistration.md, section 6, "Память"): swap grew by more than SWAP_LIMIT_GB since the run started,
or pressure stayed critical for CRITICAL_S seconds -> the configuration is recorded as "не годится для Mac mini 16 ГБ"
(runs/<id>/ABORTED.json), the process exits with code 75 before the machine hangs. harness.study treats such a run
as finished and moves on (restart the queue after the exit).
"""
from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from pathlib import Path

SWAP_LIMIT_GB = 2.0
CRITICAL_S = 10
EXIT_CODE = 75
G = 2 ** 30


def _pressure() -> int | None:
    try:
        out = subprocess.run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"],
                             capture_output=True, text=True, timeout=3).stdout.strip()
        return int(out)
    except Exception:
        return None


def start(cfg_path: Path, every: float = 1.0) -> threading.Event:
    """Start the watcher; set the returned event to stop it (run finished normally)."""
    import psutil

    stop = threading.Event()
    base = psutil.swap_memory().used / G

    def trip(reason: str, swap: float, level: int | None):
        info = {"reason": reason, "swap_gb": round(swap, 2), "swap_start_gb": round(base, 2),
                "pressure_level": level, "at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "verdict": "не годится для Mac mini 16 ГБ"}
        print(f"MEMORY GUARD: {reason}; run aborted", flush=True)
        try:
            # separate file: config.json may be mid-rewrite by the run itself
            (cfg_path.parent / "ABORTED.json").write_text(json.dumps(info, indent=1, ensure_ascii=False))
        except Exception as e:
            print(f"MEMORY GUARD: could not write ABORTED.json: {e}", flush=True)
        finally:
            os._exit(EXIT_CODE)

    def watch():
        critical_since = None
        while not stop.wait(every):
            swap = psutil.swap_memory().used / G
            level = _pressure()
            if swap - base > SWAP_LIMIT_GB:
                trip(f"swap grew {base:.2f} -> {swap:.2f} GB (> {SWAP_LIMIT_GB} GB)", swap, level)
            if level == 4:
                critical_since = critical_since or time.monotonic()
                if time.monotonic() - critical_since >= CRITICAL_S:
                    trip(f"memory pressure critical for {CRITICAL_S}+ s", swap, level)
            else:
                critical_since = None

    threading.Thread(target=watch, daemon=True).start()
    return stop
