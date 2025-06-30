# scripts/simulate_stream.py

import time
import argparse
from src.data.loader import load_csv
from src.inference.detector import Detector
from src.utils.alerts import generate_well_control_command

def simulate(file_path, interval):
    df = load_csv(file_path)
    det = Detector()

    for _, row in df.iterrows():

        data = row.drop(labels=['timestamp', 'label'], errors='ignore').to_dict()
        score, is_anom = det.predict(data)

        if is_anom:
            cmd = generate_well_control_command(data)
            print(f"🛠️ Recommendation: {cmd}")

        print(f"{row.get('timestamp', '')} → score={score:.4f}, anomaly={bool(is_anom)}")
        time.sleep(interval)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--file', default='data/raw/train.csv')
    p.add_argument('--interval', type=float, default=1.0,
                   help="Задержка в секундах между точками")
    args = p.parse_args()
    simulate(args.file, args.interval)
