# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (ffmpeg for audio streaming)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    opus-tools \
    libffi-dev \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Upgrade pip first, then install (fixes the "new release available" notice)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create dirs
RUN mkdir -p downloads/audio downloads/video cookies

# Env for unbuffered output (better logs)
ENV PYTHONUNBUFFERED=1

# Run bot
CMD ["python", "main.py"]
