BUCKET_SECONDS = 60


def bucket_start(ts: int) -> int:
    return (ts // BUCKET_SECONDS) * BUCKET_SECONDS


def count_per_bucket(events: list["Event"]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for ev in events:
        key = bucket_start(ev.ts)
        counts[key] = counts.get(key, 0) + 1
    return counts


def count_by_kind_per_bucket(events: list["Event"], kind: str) -> dict[int, int]:
    return count_per_bucket([ev for ev in events if ev.kind == kind])
