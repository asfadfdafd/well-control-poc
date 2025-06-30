import argparse
from src.data.loader import load_csv
from src.inference.detector import Detector
from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate(file_path):
    df = load_csv(file_path)
    if 'label' not in df.columns:
        print("В файле нет колонки 'label'.")
        return

    det = Detector()
    y_true = df['label'].tolist()
    y_pred = []
    for _, row in df.iterrows():
        data = row.drop(labels=['timestamp', 'label'], errors='ignore').to_dict()
        _, is_anom = det.predict(data)
        y_pred.append(is_anom)

    print("Precision:", precision_score(y_true, y_pred))
    print("Recall:",    recall_score(y_true, y_pred))
    print("F1-score:",  f1_score(y_true, y_pred))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--file', default='data/raw/test.csv')
    args = p.parse_args()
    evaluate(args.file)
