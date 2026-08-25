from dataclasses import dataclass, field


@dataclass(frozen=True)
class Event:
    ts: int          # epoch seconds
    kind: str        # e.g. "click", "signup"
    payload: dict = field(default_factory=dict)
