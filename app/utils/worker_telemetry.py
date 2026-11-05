import ctypes
import os
import platform
import psutil

# Cache once per worker process lifecycle to eliminate repeated OS syscalls
_PROCESS = psutil.Process(os.getpid())
_IS_WINDOWS = platform.system() == "Windows"


def get_worker_diagnostics(start_rss_bytes: int = None) -> dict:
    """Collects strictly dynamic runtime metrics (PID, active CPU core, RAM RSS,

    RAM delta, and thread count) in a single unified routine.
    """
    # 1. Physical RAM (Working Set / RSS)
    mem_info = _PROCESS.memory_info()
    current_rss = mem_info.rss

    # 2. Pinpoint active logical CPU core across Windows & Linux
    try:
        if _IS_WINDOWS:
            current_core = ctypes.windll.kernel32.GetCurrentProcessorNumber()
        else:
            current_core = (
                _PROCESS.cpu_num() if hasattr(_PROCESS, "cpu_num") else "N/A"
            )
    except Exception:
        current_core = "N/A"

    # 3. Dynamic metrics package
    metrics = {
        "pid": _PROCESS.pid,
        "current_cpu_core": current_core,
        "memory_rss_mb": round(current_rss / (1024 * 1024), 2),
        "threads_count": _PROCESS.num_threads(),
    }

    # 4. Optional per-request memory delta if a start timestamp/snapshot was provided
    if start_rss_bytes is not None:
        delta_mb = (current_rss - start_rss_bytes) / (1024 * 1024)
        metrics["memory_delta_mb"] = round(delta_mb, 3)

    return metrics