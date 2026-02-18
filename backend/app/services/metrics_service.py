"""Metrics service - simulated Prometheus-style metrics."""

import random
from datetime import datetime, timedelta

from app.models.schemas import MetricDataPoint, MetricsResponse


def get_simulated_metrics(
    points: int = 12,
    base_minutes_ago: int = 60,
) -> MetricsResponse:
    """Generate realistic random metrics time series.

    Returns data array for frontend chart plus latest snapshot.
    """
    now = datetime.utcnow()
    data: list[MetricDataPoint] = []

    for i in range(points):
        ts = now - timedelta(minutes=base_minutes_ago - (i * (base_minutes_ago // max(1, points - 1))))
        data.append(
            MetricDataPoint(
                timestamp=ts.isoformat() + "Z",
                cpu=round(40 + random.uniform(0, 55), 1),
                memory=round(50 + random.uniform(0, 45), 1),
                latency=round(80 + random.uniform(0, 200), 1),
                error_rate=round(random.uniform(0, 3), 2),
            )
        )

    # Latest point
    latest = data[-1] if data else MetricDataPoint(
        timestamp=now.isoformat() + "Z", cpu=50, memory=60, latency=150, error_rate=1.0
    )

    return MetricsResponse(
        data=data,
        period=f"PT{base_minutes_ago}M",
        cpu_usage=float(latest.cpu),
        memory_usage=float(latest.memory),
        latency=float(latest.latency),
        error_rate=float(latest.error_rate),
    )
