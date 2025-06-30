# src/api/main.py

from typing import Dict
from fastapi import FastAPI
from pydantic import RootModel
from datetime import datetime

from inference.detector import Detector
from utils.alerts       import alert_on_anomaly

app = FastAPI()
detector = Detector()

class DataPoint(RootModel[Dict[str, float]]):
    root: Dict[str, float]

@app.post("/detect/")
async def detect_point(dp: DataPoint):
    data = dp.root
    score, is_anom = detector.predict(data)

    if is_anom:
        top_param = max(data.items(), key=lambda kv: abs(kv[1]))[0]
        details = {
            "param": top_param,
            "value": data[top_param],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "recommendation": "Please review the affected parameter and adjust thresholds."
        }
        alert_on_anomaly(details)

    return {"anomaly_score": score, "is_anomaly": bool(is_anom)}
