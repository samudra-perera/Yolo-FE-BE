# app/endpoints/metrics.py

from fastapi import APIRouter
from datetime import timedelta
from prometheus_client import Counter, Summary, Gauge
import time

router = APIRouter()

# In-memory store for optional local usage
metrics_data = {
    "request_count": 0,
    "latencies": [],
    "start_time": time.time(),
}

inference_latency = Summary(
    "inference_latency_milliseconds", "Inference latency in milliseconds"
)

prediction_counter = Counter(
    "total_predictions_made", "Total number of successful predictions"
)

uptime_gauge = Gauge("model_uptime", "Uptime of the FastAPI app in seconds")


def track_latency(latency_ms: float):
    metrics_data["request_count"] += 1
    metrics_data["latencies"].append(latency_ms)

    inference_latency.observe(latency_ms)
    prediction_counter.inc()
    uptime_gauge.set(time.time() - metrics_data["start_time"])


def get_metrics():
    count = metrics_data["request_count"]
    latencies = metrics_data["latencies"]

    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0

    uptime_seconds = time.time() - metrics_data["start_time"]
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))
    uptime_minutes = max(uptime_seconds / 60, 1)
    request_rate = count / uptime_minutes

    return {
        "uptime": uptime_str,
        "request_rate_per_minute": round(request_rate, 2),
        "avg_latency_ms": round(avg_latency, 2),
        "max_latency_ms": round(max_latency, 2),
        "total_requests": count,
    }


@router.get("/metrics")
def read_metrics():
    return get_metrics()
