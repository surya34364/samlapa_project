import time
from fastapi import Request
from app.utils.worker_telemetry import get_worker_diagnostics


async def add_process_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    diag = get_worker_diagnostics()
    
    # Inject headers
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    response.headers["X-Worker-PID"] = str(diag["pid"])
    response.headers["X-Worker-RAM-MB"] = f"{diag['memory_rss_mb']} MB"
    response.headers["X-Worker-CPU-Core"] = str(diag["current_cpu_core"])

    return response