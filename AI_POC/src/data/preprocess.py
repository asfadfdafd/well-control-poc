# src/data/preprocess.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

FEATURES = ['Depth', 'WOB', 'SURF_RPM', 'ROP_AVG', 'PHIF', 'VSH', 'SW']

def preprocess(df: pd.DataFrame):
    missing = set(FEATURES) - set(df.columns)
    if missing:
        raise ValueError(f"Columns missing. Need more features: {missing}")

    X = df[FEATURES].astype(float).values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler
