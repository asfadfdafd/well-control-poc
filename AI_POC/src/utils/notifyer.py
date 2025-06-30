# src/utils/notifyer.py

import requests

# Жёстко прописанные токен и чат
TELEGRAM_TOKEN = "7651976618:AAFYcBRrhphrtvto2-mdP61i-defNgjFxCQ"
CHAT_ID = "392539749"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def send_telegram_message(text: str) -> None:
    resp = requests.post(API_URL, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })
    resp.raise_for_status()

# Псевдоним для alerts.py
send_telegram_notification = send_telegram_message
