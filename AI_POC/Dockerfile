FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

#RUN curl -s https://ollama.com/install.sh | bash

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

RUN python3 src/models/train.py

EXPOSE 8501

ENTRYPOINT ["bash", "-lc", "\
  ollama server start & \
  streamlit run app.py --server.port=8501 --server.address=0.0.0.0 \
"]
