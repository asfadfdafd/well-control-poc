````markdown
# Well Control Anomaly Detection POC

This project implements real-time anomaly detection for well control parameters using an Isolation Forest and generates actionable recommendations via TinyLLaMA. It also sends alerts to Telegram when anomalies are detected.

## 🐳 Docker Setup

A Docker container is provided to simplify deployment. To build and run:

```bash
# Build the Docker image
docker build -t well-control-poc .

# Run the container, mapping port 8501 for Streamlit UI
docker run -d -p 8501:8501 --name well-control-poc well-control-poc
````

After running, open [http://localhost:8501](http://localhost:8501) in your browser.

## 🔨 Dockerfile

The `Dockerfile` installs dependencies, copies the project, trains the model, and starts Streamlit:

```dockerfile
# Use Python 3.12 slim base image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama CLI
RUN curl -s https://ollama.com/install.sh | bash

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . ./

# Train model at build time
RUN python3 src/models/train.py

# Expose Streamlit port
EXPOSE 8501

# Start Ollama server and Streamlit app
ENTRYPOINT ["bash", "-lc", "ollama server start & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
```

## 📂 Data Preparation

1. Place your raw CSV data at `data/raw/train.csv`.
2. Ensure it contains the required features:

   * `Depth`, `WOB`, `SURF_RPM`, `ROP_AVG`, `PHIF`, `VSH`, `SW`,
   * `timestamp`, (optional) `label` for evaluation.
3. The Docker build will execute `src/models/train.py` to train the model using this data.

## 🚀 Running Locally (Without Docker)

To run natively:

```bash
# Install dependencies
pip install -r requirements.txt

# Train the model
python3 src/models/train.py

# Start Streamlit UI
streamlit run app.py
```

## 📜 Logs and Alerts

* **Streamlit logs** appear in the console where you run `streamlit run`.
* **Telegram alerts** are sent when anomalies are detected. Configure your bot token and chat ID in `src/utils/notifyer.py`
* or via environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

---

For detailed usage, see inline comments in `app.py`, `src/utils/alerts.py`, and `src/utils/notifyer.py`.
