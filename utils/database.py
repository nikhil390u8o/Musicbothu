# utils/database.py
from typing import Dict
queue: Dict[int, dict] = {}

def get_queue(chat_id: int):
    return queue.get(chat_id, {"tracks": [], "index": 0, "loop": False})

def add_track(chat_id: int, track: dict):
    if chat_id not in queue:
        queue[chat_id] = {"tracks": [], "index": 0, "loop": False}
    queue[chat_id]["tracks"].append(track)

def next_track(chat_id: int):
    q = queue.get(chat_id, {})
    q["index"] += 1
    if q["index"] >= len(q["tracks"]):
        if q.get("loop"):
            q["index"] = 0
        else:
            queue.pop(chat_id, None)
            return None
    return q["tracks"][q["index"]]
