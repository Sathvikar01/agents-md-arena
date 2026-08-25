"""Pipeline glue: window-filter events then aggregate per minute.

process(events, start, end) -> {"total": int, "per_minute": {bucket: n}}
where per_minute only includes buckets touched by in-window events.
"""
from window import filter_by_window
from buckets import count_per_bucket


def process(events: list, start: int, end: int) -> dict:
    kept = filter_by_window(events, start, end)
    per_minute = count_per_bucket(kept)
    return {"total": sum(per_minute.values()), "per_minute": per_minute}
