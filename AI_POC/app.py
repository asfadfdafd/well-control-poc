# app.py

import os
import time
import pandas as pd
import streamlit as st
from src.data.loader import load_csv
from src.inference.detector import Detector
from src.utils.alerts import generate_well_control_command
from src.utils.notifyer import send_telegram_message  # <-- Import уведомлений

st.set_page_config(page_title="Well Control: Anomaly Detection Stream", layout="wide")
st.title("🚀 Well Control: Anomaly Detection Stream")

DATA_FILE = "data/raw/train_with_anoms.csv"
INTERVAL = st.sidebar.slider("Интервал (сек)", 0.1, 2.0, 1.0, step=0.1)

df = load_csv(DATA_FILE)
detector = Detector()  # без искусственного порога

chart = st.line_chart()
log_area = st.empty()

for _, row in df.iterrows():
    data = row.drop(labels=['timestamp', 'label'], errors='ignore').to_dict()
    score, is_anom = detector.predict(data)

    # Обновляем график
    chart.add_rows(pd.DataFrame(
        {"score": [score]},
        index=[row['timestamp']]
    ))

    # Обновляем лог
    status = "🛑 АНОМАЛИЯ!" if is_anom else "✅ norm"
    log_area.text(f"{row['timestamp']} | score={score:.3f} | {status}")

    if is_anom:
        # 1) Генерируем рекомендацию
        with st.spinner("Генерируем рекомендацию…"):
            cmd = generate_well_control_command(data)
        st.sidebar.markdown("### Рекомендация при аномалии")
        st.sidebar.write(cmd)

        # 2) Отправляем Telegram-уведомление
        try:
            message = (
                f"🛑 *Аномалия обнаружена*\n"
                f"`{row['timestamp']}`\n"
                f"Score: `{score:.3f}`\n\n"
                f"*Рекомендация:*\n{cmd}"
            )
            send_telegram_message(message)
        except Exception as e:
            st.sidebar.error(f"Ошибка отправки Telegram: {e}")

    time.sleep(INTERVAL)
