"""Risk score service."""

import random
from datetime import datetime

from app.models.schemas import RiskScoreResponse

# Decision mapping: 0-30 Normal, 30-60 Canary, 60-100 Manual Approval
# Frontend expects: approve, reject, manual_review


def score_to_decision(score: float) -> tuple[str, str]:
    """Map risk score to decision and label.

    Returns:
        (decision, decision_label)
        decision: approve | reject | manual_review
        decision_label: Normal | Canary | Manual Approval
    """
    if score <= 30:
        return "approve", "Normal"
    if score <= 60:
        return "manual_review", "Canary"
    return "manual_review", "Manual Approval"


def get_latest_risk_score() -> RiskScoreResponse:
    """Return latest risk score with simulated values.

    Used when no ML prediction is available (e.g. GET /risk-score/latest).
    """
    score = float(random.randint(15, 85))
    decision, decision_label = score_to_decision(score)
    deployment_id = f"d{random.randint(1000, 9999)}"

    return RiskScoreResponse(
        score=score,
        risk_score=score,
        decision=decision,
        decision_label=decision_label,
        deployment_id=deployment_id,
        timestamp=datetime.utcnow(),
    )
