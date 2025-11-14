# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    opus-tools \
    libffi-dev \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create downloads & cookies dirs
RUN mkdir -p downloads/audio downloads/video cookies

# Expose nothing (bot uses Telegram API)
# EXPOSE 8000  # not needed

# Environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "main.py"]
