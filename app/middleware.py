import json
import time
from fastapi import Request
from app.utils.worker_telemetry import _PROCESS, get_worker_diagnostics


async def add_process_time(request: Request, call_next):
    # Snapshot start time and memory before request handling
    start_time = time.perf_counter()
    start_rss = _PROCESS.memory_info().rss

    response = await call_next(request)

    # Compute execution time & pass start_rss to single diagnostics function
    process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
    diagnostics = get_worker_diagnostics(start_rss_bytes=start_rss)

    # Attach dynamic metrics directly to HTTP response headers
    response.headers["X-Process-Time-ms"] = f"{process_time_ms}ms"
    response.headers["X-Worker-PID"] = str(diagnostics["pid"])
    response.headers["X-Worker-CPU-Core"] = str(diagnostics["current_cpu_core"])
    response.headers["X-Worker-RAM-RSS-MB"] = (
        f"{diagnostics['memory_rss_mb']}MB"
    )
    response.headers["X-Worker-RAM-Delta-MB"] = (
        f"{diagnostics['memory_delta_mb']:+.3f}MB"
    )
    response.headers["X-Worker-Threads-Count"] = str(
        diagnostics["threads_count"]
    )

    # Terminal log output
    log_payload = {
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "process_time_ms": f"{process_time_ms}ms",
        "worker": diagnostics,
    }

    print("\n" + "=" * 50)
    print(
        f"🚀 [{request.method}] {request.url.path} -> {response.status_code} ({process_time_ms}ms)"
    )
    print(json.dumps(log_payload, indent=2))
    print("=" * 50 + "\n")

    return response