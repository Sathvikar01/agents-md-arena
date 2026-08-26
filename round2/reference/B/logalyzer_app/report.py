"""Human-readable report rendering."""

from datetime import datetime

import parser as log_parser


def format_entry(entry):
    e = log_parser.parse_line(entry)
    if e is None:
        return "?"
    stamp = datetime.fromtimestamp(e["ts"]).strftime("%H:%M:%S")
    return f"[{stamp}] {e['level']}: {e['msg']}"


def render(lines):
    return "\n".join(format_entry(l) for l in lines)
