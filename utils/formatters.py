# utils/formatters.py
def time_to_seconds(time_str: str) -> int:
    if not time_str or time_str == "None":
        return 0
    parts = time_str.split(":")
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(parts)))
