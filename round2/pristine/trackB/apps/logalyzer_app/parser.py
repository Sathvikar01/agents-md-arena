"""Log parsing (legacy)."""

LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")


def parse_line(line):
    # format: LEVEL|epoch|message   (message may contain '|')
    parts = line.split("|", 2)
    if len(parts) != 3:
        return None
    level, ts, msg = parts
    return {"level": level, "ts": int(ts), "msg": msg.rstrip("\n")}
