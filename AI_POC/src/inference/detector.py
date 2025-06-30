# src/inference/detector.py

import pickle
import pandas as pd
from src.models.isolation_forest import IsolationForestDetector

class Detector:
    def __init__(self,
                 model_path: str = 'models/model.pkl',
                 scaler_path: str = 'models/scaler.pkl'):
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        self.features_ = getattr(self.scaler, 'feature_names_in_', None)

        self.detector = IsolationForestDetector()
        self.detector.load(model_path)

    def predict(self, data: dict):
        df = pd.DataFrame([data])

        if self.features_ is not None:
            missing = set(self.features_) - set(df.columns)
            if missing:
                raise ValueError(f"Не хватает колонок для predict: {missing}")
            df = df.loc[:, self.features_]

        X_raw = df.values.astype(float)
        X_scaled = self.scaler.transform(X_raw)

        scores, flags = self.detector.predict(X_scaled)
        score = float(scores[0])
        is_anomaly = bool(flags[0])
        return score, is_anomaly
