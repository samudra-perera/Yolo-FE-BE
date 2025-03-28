from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
def get_metrics():
    return {
        "request_rate_per_minute": 42,
        "avg_latency_ms": 153.4,
        "max_latency_ms": 312.7,
        "total_requests": 1200,
    }
