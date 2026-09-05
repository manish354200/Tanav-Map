"""Risk forecasting and explainability."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

try:
    import joblib
except Exception:  # pragma: no cover
    joblib = None

try:
    import shap
except Exception:  # pragma: no cover
    shap = None


class PredictiveRiskService:
    def __init__(self):
        self.model_dir = Path(os.getenv("PREDICTION_MODEL_DIR", "./ml/models"))
        self._models: Dict[int, object] = {}

    def _load_model(self, horizon: int):
        if horizon in self._models:
            return self._models[horizon]
        if joblib is None:
            return None
        model_path = self.model_dir / f"distress_{horizon}d.pkl"
        if model_path.exists():
            self._models[horizon] = joblib.load(model_path)
            return self._models[horizon]
        return None

    def forecast(self, feature_row: Dict[str, float], current_score: float) -> Dict[str, float]:
        horizons = [7, 15, 30]
        preds = {}
        for horizon in horizons:
            model = self._load_model(horizon)
            if model is None:
                drift = {7: 3.0, 15: 6.0, 30: 10.0}[horizon]
                preds[f"{horizon}_day_risk"] = round(min(100.0, max(0.0, current_score + drift)), 2)
                continue
            if np is None:
                preds[f"{horizon}_day_risk"] = round(min(100.0, max(0.0, current_score)), 2)
                continue
            values = np.array([[feature_row.get(k, 0.0) for k in sorted(feature_row.keys())]])
            preds[f"{horizon}_day_risk"] = round(float(model.predict(values)[0]), 2)
        return preds

    def explain(self, feature_row: Dict[str, float], current_score: float) -> List[str]:
        if shap is None:
            return [
                f"Sentiment pressure contributed {round(feature_row.get('sentiment', 0.0), 2)} points.",
                f"Voice stress contributed {round(feature_row.get('voice', 0.0), 2)} points.",
                f"Current distress score is {round(current_score, 2)}."
            ]
        summary = sorted(feature_row.items(), key=lambda item: item[1], reverse=True)[:3]
        return [f"{name} is a key risk driver ({round(value, 2)})." for name, value in summary]
