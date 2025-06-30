import subprocess
import json
import time
from .notifyer import send_telegram_notification

def ensure_ollama_server():
    # Останавливаем и сразу запускаем сервер, чтобы очистить контекст
    subprocess.run(["ollama", "stop"], capture_output=True)
    time.sleep(1)
    subprocess.run(["ollama", "server", "start"], capture_output=True)

def generate_well_control_command(data: dict) -> str:
    ensure_ollama_server()
    prompt = (
        "You are a drilling engineer assistant.\n"
        "Provide exactly 2 concise bullet-point recommendations (≤10 words each),\n"
        "with no explanations or commentary.\n\n"
        "Parameters:\n" +
        json.dumps(data, separators=(',', ':'), ensure_ascii=False) +
        "\n\nRecommendations:\n"
        "1.\n"
        "2.\n"
    )
    try:
        res = subprocess.run(
            ["ollama", "run", "tinyllama", prompt],
            capture_output=True, text=True
        )
        if res.returncode != 0:
            return f"[Ollama error: {res.stderr.strip()}]"

        # Отбираем только пункты 1. и 2.
        lines = [l.strip() for l in res.stdout.splitlines()]
        recs = [l for l in lines if l.startswith("1.") or l.startswith("2.")]
        return "\n".join(recs) or res.stdout.strip()
    except FileNotFoundError:
        return "[Ollama CLI not found—install and run `ollama server start`]"
    except Exception as e:
        return f"[Exception during recommendation: {e}]"

from .notifyer import send_telegram_notification

def alert_on_anomaly(details: dict) -> None:
    lines = [
        "*⚠️ Anomaly detected!*",
        f"• *Parameter:* `{details['param']}`",
        f"• *Value:* `{details['value']}`",
        f"• *Time:* `{details['timestamp']}`"
    ]
    if details.get("recommendation"):
        lines.append(f"\n*💡 Recommendation:* {details['recommendation']}")
    message = "\n".join(lines)
    send_telegram_notification(message)
