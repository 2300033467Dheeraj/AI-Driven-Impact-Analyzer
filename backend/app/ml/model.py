"""ML risk prediction model with optional scikit-learn fallback."""

from pathlib import Path
import numpy as np

from app.ml.feature_engineering import FEATURE_NAMES

# Optional sklearn - avoid build on Windows + Python 3.13
try:
    from sklearn.ensemble import RandomForestClassifier

    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    RandomForestClassifier = None  # type: ignore

try:
    import joblib
except ImportError:
    joblib = None

# Risk class mapping
CLASS_TO_DECISION = {
    0: "approve",
    1: "manual_review",
    2: "manual_review",
}
CLASS_TO_LABEL = {
    0: "Normal",
    1: "Canary",
    2: "Manual Approval",
}


def _heuristic_score(features: np.ndarray) -> tuple[float, str, str]:
    """Rule-based risk when scikit-learn is unavailable (e.g. Windows + Python 3.13)."""
    # features: [files_changed, critical_service_modified, dependency_depth, cpu, latency, error_rate]
    f = features[0]
    files_changed = f[0]
    critical = f[1]
    depth = f[2]
    cpu = f[3]
    latency = f[4]
    error_rate = f[5]

    score = (
        files_changed * 0.5
        + critical * 25
        + depth * 3
        + cpu * 0.2
        + latency * 0.03
        + error_rate * 5
    )
    score = min(100, max(0, score))

    if score <= 30:
        return float(score), "approve", "Normal"
    if score <= 60:
        return float(score), "manual_review", "Canary"
    return float(score), "manual_review", "Manual Approval"


class RiskPredictor:
    """RandomForest-based or heuristic risk predictor."""

    def __init__(self, model: "RandomForestClassifier | None" = None):
        self.model = model
        if model is None and HAS_SKLEARN:
            self.model = RandomForestClassifier(
                n_estimators=100, max_depth=10, random_state=42
            )

    def predict_risk_score(self, features: np.ndarray) -> tuple[float, str, str]:
        """Predict risk score (0-100) and decision."""
        if not HAS_SKLEARN or self.model is None:
            return _heuristic_score(features)

        try:
            pred_class = int(self.model.predict(features)[0])
        except Exception:
            return _heuristic_score(features)

        decision = CLASS_TO_DECISION.get(pred_class, "manual_review")
        decision_label = CLASS_TO_LABEL.get(pred_class, "Manual Approval")

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(features)[0]
            base_scores = {0: 15, 1: 45, 2: 75}
            base = base_scores.get(pred_class, 50)
            confidence = float(max(probs)) if len(probs) > 0 else 0.5
            risk_score = min(100, max(0, base + (confidence - 0.5) * 40))
        else:
            risk_score = {0: 20, 1: 45, 2: 75}.get(pred_class, 50)

        return float(risk_score), decision, decision_label

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RiskPredictor":
        """Train the model (sklearn only)."""
        if HAS_SKLEARN and self.model is not None:
            self.model.fit(X, y)
        return self

    def save(self, path: Path) -> None:
        """Save model (sklearn only)."""
        if not HAS_SKLEARN or self.model is None or joblib is None:
            return
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": self.model, "feature_names": FEATURE_NAMES}, path)

    @classmethod
    def load(cls, path: Path) -> "RiskPredictor":
        """Load model from disk or return heuristic fallback."""
        path = Path(path)
        if HAS_SKLEARN and joblib is not None and path.exists():
            try:
                data = joblib.load(path)
                model = data.get("model")
                if model is not None:
                    return cls(model=model)
            except Exception:
                pass
        return cls(model=None)
