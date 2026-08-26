"""Log parsing."""

LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")


def parse_line(line: str):
    parts = line.split("|", maxsplit=2)
    if len(parts) != 3:
        return None
    level, ts, msg = parts
    return {"level": level, "ts": int(ts), "msg": msg.rstrip("\n")}
