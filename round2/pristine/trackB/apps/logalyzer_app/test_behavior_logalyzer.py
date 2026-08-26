"""CHARACTERIZATION TESTS - locked behavior for logalyzer_app. DO NOT MODIFY."""

import report
import stats
import parser

SAMPLE = [
    "INFO|1700000000|service started",
    "ERROR|1700000030|db conn failed: retry=1",
    "INFO|1700000059|warmed up",
    "WARN|1700000061|slow query",
    "ERROR|1700000061|panic in worker|segment ignored",
]


def test_parse_basic():
    e = parser.parse_line("INFO|1700000000|hello")
    assert e == {"level": "INFO", "ts": 1700000000, "msg": "hello"}


def test_parse_message_with_pipes():
    e = parser.parse_line(SAMPLE[4])
    assert e["msg"] == "panic in worker|segment ignored"


def test_parse_strips_newline_only():
    e = parser.parse_line("WARN|5|x\n")
    assert e["msg"] == "x" and e["ts"] == 5


def test_malformed_returns_none():
    assert parser.parse_line("nope") is None
    assert parser.parse_line("A|1") is None


def test_level_counts():
    assert stats.level_counts(SAMPLE) == {"INFO": 2, "ERROR": 2, "WARN": 1}


def test_minute_buckets_floor():
    mc = stats.minute_counts(SAMPLE)
    assert mc[1699999980] == 2
    assert mc[1700000040] == 3


def test_format_entry():
    out = report.format_entry("INFO|1700000000|hi")
    assert "] INFO: hi" in out


def test_render_joins_newlines():
    r = report.render(["INFO|1700000000|a", "ERROR|1700000001|b"])
    assert r.count("\n") == 1 and "a" in r and "b" in r


def test_render_bad_line_placeholder():
    assert report.render(["junk"]) == "?"


def test_summary_shape():
    # R5 renames f -> summarize; accept either so the rename stays allowed
    summarize = getattr(stats, "summarize", None) or stats.f
    s = summarize(SAMPLE)
    assert set(s) == {"levels", "minutes", "busiest"}
    assert s["busiest"] == 3
