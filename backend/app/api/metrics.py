"""Metrics API routes."""

from fastapi import APIRouter

from app.models.schemas import MetricsResponse
from app.services.metrics_service import get_simulated_metrics

router = APIRouter(tags=["metrics"])


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics() -> MetricsResponse:
    """Return simulated Prometheus-style metrics.

    Frontend expects: data array of { timestamp, latency, error_rate, cpu, memory }.
    """
    return get_simulated_metrics(points=12, base_minutes_ago=60)
