# youtube.py
import asyncio
import os
import re
import json
import random
import aiohttp
import yt_dlp
from pathlib import Path
from typing import Union
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType
from youtubesearchpython.__future__ import VideosSearch
from utils.formatters import time_to_seconds
import config

async def fetch_stream_url(link: str, video: bool = False) -> str | None:
    try:
        video_id = link.split("v=")[-1].split("&")[0]
    except:
        return None

    url = f"{config.API_URL}/song/{video_id}?key={config.API_KEY}"
    if video:
        url += "&video=True"

    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for _ in range(2):
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "done":
                            return data.get("stream_url")
            except:
                await asyncio.sleep(0.5)
    return None

async def download_file(link: str, video: bool = False) -> str | None:
    try:
        video_id = link.split("v=")[-1].split("&")[0]
    except:
        return None

    folder = Path("downloads/video" if video else "downloads/audio")
    folder.mkdir(parents=True, exist_ok=True)
    ext = ".mp4" if video else ".m4a"
    filepath = folder / f"{video_id}{ext}"
    temp_path = filepath.with_suffix(".part")

    if filepath.exists():
        return str(filepath)

    stream_url = await fetch_stream_url(link, video=video)
    if not stream_url:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(stream_url) as resp:
            if resp.status != 200:
                return None
            with open(temp_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024*1024):
                    f.write(chunk)
    temp_path.rename(filepath)
    return str(filepath)

def cookie_txt_file():
    cookie_dir = "cookies"
    if not os.path.exists(cookie_dir):
        return None
    files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    return os.path.join(cookie_dir, random.choice(files)) if files else None

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset:entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return (
                result["title"],
                result["duration"],
                time_to_seconds(result["duration"]),
                result["thumbnails"][0]["url"].split("?")[0],
                result["id"]
            )

    async def download(self, link: str, video: bool = False) -> tuple:
        if videoid:
            link = self.base + link
        # Try API first
        try:
            file = await download_file(link, video=video)
            if file:
                return file, True
        except:
            pass

        # Fallback: yt-dlp
        cookie_file = cookie_txt_file()
        if not cookie_file:
            return None, None

        ydl_opts = {
            "format": "bestaudio" if not video else "best[height<=720]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "cookiefile": cookie_file,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            url = info["url"]
            return url, False
