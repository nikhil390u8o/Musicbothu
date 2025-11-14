# Dockerfile
# Dockerfile (No Changes Needed)
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    opus-tools \
    libffi-dev \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir --trusted-host pypi.org -r requirements.txt

COPY . .

RUN mkdir -p downloads/audio downloads/video cookies

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
