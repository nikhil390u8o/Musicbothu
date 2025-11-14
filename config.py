# config.py
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = os.getenv("SESSION_NAME", "musicbot")
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "1800"))minutes
