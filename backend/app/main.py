from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.endpoints import predict, health, management, metrics, group
from app.endpoints import evaluate
import time

app = FastAPI()

startup_time = time.time()

# Enable CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route includes
app.include_router(predict.router)
app.include_router(evaluate.router)
app.include_router(health.get_router(startup_time))
app.include_router(management.router)
app.include_router(metrics.router)
app.include_router(group.router)

# Instrument app
Instrumentator().instrument(app).expose(app)
