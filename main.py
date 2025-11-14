# main.py (Key Changes Only – Replace Relevant Sections)
# main.py
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# <-- CORRECT IMPORT (underscore) ------------------------------------
from py_tgcalls import PyTgCalls, StreamType
from py_tgcalls.types import AudioPiped
# ---------------------------------------------------------------------

from youtubesearchpython.__future__ import VideosSearch
from utils.formatters import time_to_seconds
import config
from youtube import YouTubeAPI
from utils.database import add_track, get_queue, next_track

app = Client(
    config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

pytgcalls = PyTgCalls(app)
youtube = YouTubeAPI()

os.makedirs("downloads/audio", exist_ok=True)
os.makedirs("downloads/video", exist_ok=True)


async def get_stream(link: str):
    file, direct = await youtube.download(link)
    return file


@app.on_message(filters.command("play") & filters.group)
async def play(_, m):
    if pytgcalls.is_in_call(m.chat.id):
        return await m.reply("Already playing! Use /queue")

    link = await youtube.url(m)
    if not link:
        query = m.text.split(maxsplit=1)[1] if len(m.text.split()) > 1 else None
        if query:
            vs = VideosSearch(query, limit=1)
            result = (await vs.next())["result"]
            if result:
                link = result[0]["link"]
            else:
                return await m.reply("No results found.")
        else:
            return await m.reply("Send a link or search query.")

    try:
        title, dur, _, thumb, vid = await youtube.details(link)
    except Exception as e:
        return await m.reply(f"Failed to fetch info: {e}")

    if time_to_seconds(dur) > config.DURATION_LIMIT:
        return await m.reply("Track too long!")

    track = {
        "title": title,
        "dur": dur,
        "thumb": thumb,
        "link": link,
        "by": m.from_user.mention,
    }
    add_track(m.chat.id, track)

    await m.reply(f"**Now Playing:**\n`{title}`\n`{dur}`")
    await pytgcalls.join_group_call(
        m.chat.id,
        AudioPiped(await get_stream(link)),
        stream_type=StreamType().pulse_stream,
    )


@pytgcalls.on_stream_end()
async def next_song(_, update):
    chat_id = update.chat_id
    nxt = next_track(chat_id)
    if nxt:
        await pytgcalls.change_stream(
            chat_id, AudioPiped(await get_stream(nxt["link"]))
        )


@app.on_message(filters.command("skip"))
async def skip(_, m):
    if pytgcalls.is_in_call(m.chat.id):
        nxt = next_track(m.chat.id)
        if nxt:
            await pytgcalls.change_stream(
                m.chat.id, AudioPiped(await get_stream(nxt["link"]))
            )
            await m.reply("Skipped!")
        else:
            await pytgcalls.leave_group_call(m.chat.id)
            await m.reply("Queue ended.")


@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply(
        "Music Bot with DeadlineTech API\n\n"
        "/play [link/search] – Play music\n"
        "/skip – Skip track",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Source", url="https://github.com/nikhil390u8o/Musicbothu")]]
        ),
    )


if __name__ == "__main__":
    app.start()
    pytgcalls.start()
    print("Bot started and running forever!")  # Yeh log me dikhega
    app.idle()  # Yeh line bot ko alive rakhegi – MUST!  # ← Use idle() for long-running
