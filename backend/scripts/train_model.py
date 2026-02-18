"""Train RandomForest risk prediction model with mock data."""

import sys
from pathlib import Path

import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ml.feature_engineering import FEATURE_NAMES
from app.ml.model import RiskPredictor


def generate_mock_training_data(
    n_samples: int = 500,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate mock training data.

    Features: files_changed, critical_service_modified, dependency_depth,
              cpu_usage, latency, error_rate
    Target: 0 (low), 1 (medium), 2 (high risk)
    """
    rng = np.random.default_rng(random_state)

    X = np.zeros((n_samples, len(FEATURE_NAMES)))

    # files_changed: 1-50
    X[:, 0] = rng.integers(1, 51, n_samples)

    # critical_service_modified: 0 or 1
    X[:, 1] = rng.choice([0, 1], n_samples)

    # dependency_depth: 0-10
    X[:, 2] = rng.integers(0, 11, n_samples)

    # cpu_usage: 20-95
    X[:, 3] = rng.uniform(20, 95, n_samples)

    # latency: 50-500 ms
    X[:, 4] = rng.uniform(50, 500, n_samples)

    # error_rate: 0-5
    X[:, 5] = rng.uniform(0, 5, n_samples)

    # Target: heuristic risk class
    # 0: low (approve), 1: medium (canary), 2: high (manual)
    risk_score = (
        X[:, 0] * 0.5
        + X[:, 1] * 25
        + X[:, 2] * 3
        + X[:, 3] * 0.3
        + X[:, 4] * 0.05
        + X[:, 5] * 5
    )
    y = np.zeros(n_samples, dtype=int)
    y[risk_score < 30] = 0
    y[(risk_score >= 30) & (risk_score < 60)] = 1
    y[risk_score >= 60] = 2

    return X, y


def main() -> None:
    """Train and save model. Skips if scikit-learn unavailable (e.g. Windows + Python 3.13)."""
    from app.ml.model import HAS_SKLEARN

    if not HAS_SKLEARN:
        print("scikit-learn not available (install on Python 3.11/3.12 for ML). Using heuristic fallback.")
        return

    model_path = Path(__file__).resolve().parent.parent / "app" / "ml" / "model.joblib"

    print("Generating mock training data...")
    X, y = generate_mock_training_data(n_samples=500)

    print(f"Training samples: {X.shape[0]}")
    print(f"Class distribution: {np.bincount(y)}")

    predictor = RiskPredictor()
    predictor.fit(X, y)
    predictor.save(model_path)

    print(f"Model saved to {model_path}")

    # Quick validation
    sample = X[:1]
    score, decision, label = predictor.predict_risk_score(sample)
    print(f"Sample prediction: score={score:.1f}, decision={decision}, label={label}")


if __name__ == "__main__":
    main()
