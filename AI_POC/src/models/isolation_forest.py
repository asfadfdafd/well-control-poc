import pickle
from sklearn.ensemble import IsolationForest

class IsolationForestDetector:
    def __init__(self, **kwargs):
        self.model = IsolationForest(**kwargs)

    def fit(self, X):
        self.model.fit(X)

    def predict(self, X):
        # decision_function: чем ниже score, тем сильнее аномалия
        scores = self.model.decision_function(X)
        raw = self.model.predict(X)  # -1 = anomaly, 1 = normal
        flags = [1 if r == -1 else 0 for r in raw]
        return scores, flags

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, path: str):
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
