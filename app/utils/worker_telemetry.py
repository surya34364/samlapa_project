import os
import psutil
def get_worker_diagnostics() -> dict:
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    # CPU core affinity (on Windows/Linux, shows allowed or active CPU IDs)
    try:
        cpu_affinity = process.cpu_affinity()
    except (AttributeError, psutil.AccessDenied):
        cpu_affinity = []

    # Active CPU core number (Linux/Unix); fallback on Windows
    try:
        current_cpu = (
            process.cpu_num() if hasattr(process, "cpu_num") else "N/A"
        )
    except Exception:
        current_cpu = "N/A"

    return {
        "pid": process.pid,
        "parent_pid": os.getppid(),
        "memory_rss_mb": round(mem_info.rss / (1024 * 1024), 2),
        "memory_vms_mb": round(mem_info.vms / (1024 * 1024), 2),
        "memory_percent": round(process.memory_percent(), 2),
        "cpu_affinity": cpu_affinity,
        "current_cpu_core": current_cpu,
        "threads_count": process.num_threads(),
    }