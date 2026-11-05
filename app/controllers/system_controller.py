# from fastapi import APIRouter
# from app.utils.worker_telemetry import get_worker_diagnostics

# router = APIRouter(tags=["System Testing"])

# @router.get("/worker-status")
# def worker_status():
#     """Returns detailed process, memory, and core affinity for the worker handling this request."""
#     return get_worker_diagnostics()