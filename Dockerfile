# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (ffmpeg for streaming)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    opus-tools \
    libffi-dev \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Upgrade pip and install in virtualenv (with trusted host for reliability)
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir --trusted-host pypi.org -r requirements.txt

# Copy source code
COPY . .

# Create persistent dirs
RUN mkdir -p downloads/audio downloads/video cookies

# Activate virtualenv and set env
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Run bot
CMD ["python", "main.py"]
