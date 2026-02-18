"""FastAPI dependencies."""

from functools import lru_cache
from pathlib import Path

from app.config import get_settings
from app.ml.model import RiskPredictor


@lru_cache
def get_risk_predictor() -> RiskPredictor:
    """Load ML model at startup."""
    settings = get_settings()
    model_path = settings.model_path_resolved
    return RiskPredictor.load(model_path)


def get_settings_dep():
    """Settings dependency."""
    return get_settings()
