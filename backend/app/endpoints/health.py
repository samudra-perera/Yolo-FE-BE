from fastapi import APIRouter
from datetime import timedelta
import time


def get_router(start_time: float):
    router = APIRouter()

    @router.get("/health-status")
    def health_check():
        uptime_seconds = time.time() - start_time
        uptime_str = str(timedelta(seconds=int(uptime_seconds)))

        return {"status": "Healthy", "server": "FastAPI", "uptime": uptime_str}

    return router
