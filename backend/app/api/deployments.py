"""Deployments API - for frontend compatibility and manual data."""

import random
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from app.models.schemas import AddDeploymentRequest

router = APIRouter(tags=["deployments"])

# In-memory store for manually added deployments (persists until server restart)
_deployments_store: list[dict] = []


def _mock_deployments() -> list[dict]:
    """Generate mock deployments when store is empty or for fill."""
    services = [
        "auth-service",
        "payment-gateway",
        "user-profile-api",
        "notification-service",
        "search-indexer",
        "order-service",
        "inventory-service",
    ]
    statuses = ["success", "failed", "pending"]
    now = datetime.utcnow()
    result = []
    for i in range(7):
        risk = random.randint(15, 85)
        dec = "approve" if risk <= 30 else "manual_review"
        result.append({
            "id": f"dep-mock-{1000 + i}",
            "service_name": services[i % len(services)],
            "risk_score": risk,
            "decision": dec,
            "timestamp": (now - timedelta(hours=i + 1)).isoformat() + "Z",
            "status": statuses[i % 3],
        })
    return result


@router.get("/deployments")
def get_deployments():
    """Return deployment history: manually added first, then mock data.

    Frontend expects: id, service_name, risk_score, decision, timestamp, status.
    """
    # Manually added deployments first (newest first)
    stored = sorted(_deployments_store, key=lambda x: x["timestamp"], reverse=True)
    if stored:
        return stored + _mock_deployments()
    return _mock_deployments()


@router.post("/deployments")
def add_deployment(request: AddDeploymentRequest):
    """Manually add a deployment. Stored in memory (lost on restart)."""
    deployment_id = f"dep-{uuid.uuid4().hex[:8]}"
    entry = {
        "id": deployment_id,
        "service_name": request.service_name,
        "risk_score": request.risk_score,
        "decision": request.decision,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": request.status,
    }
    _deployments_store.append(entry)
    return {"id": deployment_id, "message": "Deployment added", "deployment": entry}
