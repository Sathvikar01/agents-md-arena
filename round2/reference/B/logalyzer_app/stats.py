"""Aggregations."""

import consts
import parser


def _bucket(ts: int) -> int:
    return ts // consts.MINUTE_SECONDS * consts.MINUTE_SECONDS


class LogStats:
    def __init__(self, lines):
        self._lines = lines

    def levels(self):
        counts = {}
        for line in self._lines:
            e = parser.parse_line(line)
            if e is None:
                continue
            counts[e["level"]] = counts.get(e["level"], 0) + 1
        return counts

    def minutes(self):
        counts = {}
        for line in self._lines:
            e = parser.parse_line(line)
            if e is None:
                continue
            b = _bucket(e["ts"])
            counts[b] = counts.get(b, 0) + 1
        return counts


def level_counts(lines):
    return LogStats(lines).levels()


def minute_counts(lines):
    return LogStats(lines).minutes()


def summarize(lines):
    lc = LogStats(lines).levels()
    mc = LogStats(lines).minutes()
    return {"levels": lc, "minutes": mc, "busiest": max(mc.values(), default=0)}
