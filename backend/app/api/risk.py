"""Risk score API routes."""

from fastapi import APIRouter

from app.models.schemas import RiskScoreResponse
from app.services.risk_service import get_latest_risk_score

router = APIRouter(prefix="/risk-score", tags=["risk"])


@router.get("/latest", response_model=RiskScoreResponse)
def get_risk_score_latest() -> RiskScoreResponse:
    """Return latest risk score with simulated values.

    Frontend expects: score, decision (approve|reject|manual_review),
    timestamp?, deployment_id?
    """
    return get_latest_risk_score()
