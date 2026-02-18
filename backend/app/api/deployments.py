"""Deployments API - for frontend compatibility."""

import random
from datetime import datetime, timedelta

from fastapi import APIRouter

router = APIRouter(tags=["deployments"])


@router.get("/deployments")
def get_deployments():
    """Return simulated deployment history for frontend table.

    Frontend expects: id, service_name, risk_score, decision,
    timestamp, status (success|failed|pending).
    """
    services = [
        "auth-service",
        "payment-gateway",
        "user-profile-api",
        "notification-service",
        "search-indexer",
        "order-service",
        "inventory-service",
    ]
    decisions = ["approve", "reject", "manual_review"]
    statuses = ["success", "failed", "pending"]

    now = datetime.utcnow()
    result = []
    for i in range(7):
        risk = random.randint(15, 85)
        if risk <= 30:
            dec = "approve"
        elif risk <= 60:
            dec = "manual_review"
        else:
            dec = "manual_review"
        status = statuses[i % 3]
        result.append({
            "id": f"dep-{1000 + i}",
            "service_name": services[i % len(services)],
            "risk_score": risk,
            "decision": dec,
            "timestamp": (now - timedelta(hours=i + 1)).isoformat() + "Z",
            "status": status,
        })
    return result
