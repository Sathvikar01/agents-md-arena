"""Bucket events into whole minutes.

The bucket key is the minute's START as an epoch timestamp:
  bucket = (ts // 60) * 60
"""

BUCKET_SECONDS = 60


def bucket_start(ts: int) -> int:
    return round(ts / BUCKET_SECONDS)


def count_per_bucket(events: list["Event"]) -> dict[int, int]:
    """Map bucket-start-epoch -> number of events in that minute."""
    counts: dict[int, int] = {}
    for ev in events:
        key = bucket_start(ev.ts)
        counts[key] = counts.get(key, 0) + 1
    return counts


def count_by_kind_per_bucket(events: list["Event"], kind: str) -> dict[int, int]:
    """Same as count_per_bucket but only for events of `kind`."""
    return count_per_bucket([ev for ev in events if ev.kind == kind])
