# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# ---- system deps (ffmpeg is required for voice-chat streaming) ----
RUN apt-get update && apt-get install -y \
    ffmpeg \
    opus-tools \
    libffi-dev \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

# ---- upgrade pip once ------------------------------------------------
RUN pip install --upgrade pip

# ---- install Python packages (system-wide) ---------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- copy the bot code ------------------------------------------------
COPY . .

# ---- persistent folders (will be volumes) ----------------------------
RUN mkdir -p downloads/audio downloads/video cookies

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
CMD ["python", "debug.py"]
