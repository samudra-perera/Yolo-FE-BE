from fastapi import APIRouter
from datetime import datetime, timedelta
import time

router = APIRouter()

# Store metrics in memory
metrics_data = {
    "request_count": 0,
    "latencies": [],
    "start_time": time.time(),
}


def track_latency(latency_ms):
    metrics_data["request_count"] += 1
    metrics_data["latencies"].append(latency_ms)


def get_metrics():
    count = metrics_data["request_count"]
    latencies = metrics_data["latencies"]

    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0

    uptime_seconds = time.time() - metrics_data["start_time"]
    uptime_minutes = max(uptime_seconds / 60, 1)  # avoid division by 0
    request_rate = count / uptime_minutes

    return {
        "request_rate_per_minute": round(request_rate),
        "avg_latency_ms": round(avg_latency, 2),
        "max_latency_ms": round(max_latency, 2),
        "total_requests": count,
    }


@router.get("/metrics")
def read_metrics():
    return get_metrics()
