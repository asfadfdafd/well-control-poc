# src/models/train.py

import os
import pickle
from src.data.loader import load_csv
from src.data.preprocess import preprocess
from src.models.isolation_forest import IsolationForestDetector

def train():
    df = load_csv('data/raw/train.csv')

    X_scaled, scaler = preprocess(df)

    detector = IsolationForestDetector(n_estimators=100, contamination=0.10)
    detector.fit(X_scaled)

    os.makedirs('models', exist_ok=True)
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    detector.save('models/model.pkl')
    print("Training done. Модель и scaler сохранены в /models.")

if __name__ == "__main__":
    train()
