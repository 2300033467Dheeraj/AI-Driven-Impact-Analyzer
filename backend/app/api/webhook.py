"""Webhook and analyze-deployment API routes."""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends

from app.dependencies import get_risk_predictor
from app.ml.feature_engineering import build_feature_vector, feature_dict
from app.ml.model import RiskPredictor
from app.models.schemas import (
    AnalyzeDeploymentRequest,
    AnalyzeDeploymentResponse,
    GitHubWebhookPayload,
)
from app.services.metrics_service import get_simulated_metrics
router = APIRouter(tags=["webhook", "analyze"])


@router.post("/analyze-deployment", response_model=AnalyzeDeploymentResponse)
def analyze_deployment(
    request: AnalyzeDeploymentRequest,
    predictor: RiskPredictor = Depends(get_risk_predictor),
) -> AnalyzeDeploymentResponse:
    """Analyze deployment risk using ML model.

    - Fetch current metrics
    - Build feature vector
    - Predict risk
    """
    metrics = get_simulated_metrics(points=1, base_minutes_ago=0)
    latest = metrics.data[-1] if metrics.data else None

    cpu = latest.cpu if latest else 50.0
    latency = latest.latency if latest else 150.0
    error_rate = latest.error_rate if latest else 1.0

    features = build_feature_vector(request, cpu, latency, error_rate)
    score, decision, decision_label = predictor.predict_risk_score(features)

    deployment_id = f"dep-{uuid.uuid4().hex[:8]}"

    return AnalyzeDeploymentResponse(
        risk_score=score,
        decision=decision,
        decision_label=decision_label,
        deployment_id=deployment_id,
        features_used=feature_dict(request, cpu, latency, error_rate),
    )


@router.post("/webhook/github")
def github_webhook(payload: GitHubWebhookPayload) -> dict:
    """Accept GitHub webhook (push) and trigger risk analysis.

    Extracts commit metadata and returns analysis result.
    """
    commits = payload.commits or []
    head = payload.head_commit
    if head:
        commits = [head]

    files_changed = 0
    critical_service_modified = False
    critical_services = {"auth", "payment", "order", "user"}

    for c in commits:
        files_changed += len(c.added) + len(c.modified) + len(c.removed)
        for f in c.added + c.modified + c.removed:
            f_lower = f.lower()
            if any(s in f_lower for s in critical_services):
                critical_service_modified = True

    if files_changed == 0:
        files_changed = 1

    # Simplified analysis
    request = AnalyzeDeploymentRequest(
        files_changed=files_changed,
        critical_service_modified=critical_service_modified,
        dependency_depth=3,
    )
    metrics = get_simulated_metrics(points=1, base_minutes_ago=0)
    latest = metrics.data[-1] if metrics.data else None
    cpu = latest.cpu if latest else 50.0
    latency = latest.latency if latest else 150.0
    error_rate = latest.error_rate if latest else 1.0

    predictor = get_risk_predictor()
    features = build_feature_vector(request, cpu, latency, error_rate)
    score, decision, decision_label = predictor.predict_risk_score(features)

    return {
        "event": "push",
        "files_changed": files_changed,
        "critical_service_modified": critical_service_modified,
        "risk_score": score,
        "decision": decision,
        "decision_label": decision_label,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
