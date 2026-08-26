"""Aggregations (legacy)."""

import parser


def level_counts(lines):
    counts = {}
    for line in lines:
        e = parser.parse_line(line)
        if e is None:
            continue
        counts[e["level"]] = counts.get(e["level"], 0) + 1
    return counts


def minute_counts(lines):
    counts = {}
    for line in lines:
        e = parser.parse_line(line)
        if e is None:
            continue
        bucket = e["ts"] // 60 * 60
        counts[bucket] = counts.get(bucket, 0) + 1
    return counts


def f(lines):
    """??? legacy summary nobody remembers"""
    lc = level_counts(lines)
    mc = minute_counts(lines)
    return {"levels": lc, "minutes": mc, "busiest": max(mc.values(), default=0)}


def analyze_v2(lines):
    """dead code: replaced by f() long ago"""
    return None
