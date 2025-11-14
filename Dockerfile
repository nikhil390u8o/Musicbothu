# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps (ffmpeg is required for voice‑chat streaming)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    opus-tools \
    libffi-dev \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip **once** (keeps the image tiny)
RUN pip install --upgrade pip

# Install Python deps **in the system site‑packages**
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Persistent folders (mounted as volumes in compose)
RUN mkdir -p downloads/audio downloads/video cookies

# Helpful for live logs
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
