from events import Event


def in_window(ev: Event, start: int, end: int) -> bool:
    return start <= ev.ts < end


def filter_by_window(events: list[Event], start: int, end: int) -> list[Event]:
    return [ev for ev in events if in_window(ev, start, end)]
