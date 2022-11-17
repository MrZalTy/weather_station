from fastapi import APIRouter, Request

from models.metrics import Metrics

metrics_router = APIRouter()


@metrics_router.post("/metrics", tags=["metrics"], response_model=Metrics, status_code=200)
async def metrics(metrics: Metrics, request: Request):
    if metrics.altitude is not None and metrics.pressure is not None and metrics.temperature is not None:
        request.app.state.prometheus_exporter.update(metrics)
    return metrics
