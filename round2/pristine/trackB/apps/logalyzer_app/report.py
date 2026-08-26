"""Human-readable report rendering (legacy copy-paste)."""


def format_entry(entry):
    # NOTE: duplicated parse logic with parser.parse_line - keep in sync!
    parts = entry.split("|", 2)
    if len(parts) != 3:
        return "?"
    level, ts, msg = parts
    msg = msg.rstrip("\n")
    from datetime import datetime as _dt

    stamp = _dt.fromtimestamp(int(ts)).strftime("%H:%M:%S")
    return f"[{stamp}] {level}: {msg}"


def render(lines):
    out = []
    for line in lines:
        out.append(format_entry(line))
    return "\n".join(out)
