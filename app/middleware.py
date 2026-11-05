import json
import logging
import time
from fastapi import Request
from app.utils.worker_telemetry import get_worker_diagnostics

logger = logging.getLogger("worker_telemetry")
logging.basicConfig(level=logging.INFO)


async def add_process_time(request: Request, call_next):
    start_time = time.perf_counter()

    # Process the request through routers/endpoints
    response = await call_next(request)

    # Calculate execution time
    process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

    # Collect process & worker stats
    diagnostics = get_worker_diagnostics()

    # Format output for terminal logs
    log_payload = {
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "process_time_ms": f"{process_time_ms}ms",
        "worker_metrics": diagnostics,
    }

    # Print directly to terminal
    print(f"🚀 [{request.method}] {request.url.path} -> {response.status_code} ({process_time_ms}ms)")
    print(json.dumps(log_payload, indent=2))

    return response