"""Feature engineering for risk prediction."""

import numpy as np

from app.models.schemas import AnalyzeDeploymentRequest

# Feature names in order expected by the model
FEATURE_NAMES = [
    "files_changed",
    "critical_service_modified",
    "dependency_depth",
    "cpu_usage",
    "latency",
    "error_rate",
]


def build_feature_vector(
    request: AnalyzeDeploymentRequest,
    cpu_usage: float,
    latency: float,
    error_rate: float,
) -> np.ndarray:
    """Build feature vector for ML prediction.

    Features:
    - files_changed
    - critical_service_modified (0/1)
    - dependency_depth
    - cpu_usage
    - latency
    - error_rate
    """
    return np.array(
        [
            float(request.files_changed),
            1.0 if request.critical_service_modified else 0.0,
            float(request.dependency_depth),
            cpu_usage,
            latency,
            error_rate,
        ],
        dtype=np.float64,
    ).reshape(1, -1)


def feature_dict(
    request: AnalyzeDeploymentRequest,
    cpu_usage: float,
    latency: float,
    error_rate: float,
) -> dict[str, float]:
    """Return features as dict for logging/response."""
    return {
        "files_changed": float(request.files_changed),
        "critical_service_modified": 1.0 if request.critical_service_modified else 0.0,
        "dependency_depth": float(request.dependency_depth),
        "cpu_usage": cpu_usage,
        "latency": latency,
        "error_rate": error_rate,
    }
