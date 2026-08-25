import pytest
from csv_stats import parse_csv, column_stats

CSV = "name,score\nann,10\nbob,\ncat,7\n"


def test_parse_rows_exclude_header():
    rows = parse_csv(CSV)
    assert len(rows) == 3
    assert rows[1]["name"] == "bob"
    assert set(rows[0].keys()) == {"name", "score"}


def test_stats_basic():
    rows = parse_csv("v\n1\n2\n3\n")
    s = column_stats(rows, "v")
    assert s == {"min": 1.0, "max": 3.0, "avg": 2.0}


def test_stats_skip_blank_cells():
    rows = parse_csv('v\n4\n""\n8\n')
    assert column_stats(rows, "v")["avg"] == 6.0


def test_stats_single_value():
    rows = parse_csv("v\n5\n")
    assert column_stats(rows, "v") == {"min": 5.0, "max": 5.0, "avg": 5.0}


def test_missing_column_raises():
    with pytest.raises(KeyError):
        column_stats([{"a": "1"}], "nope")


def test_all_blank_raises_valueerror():
    rows = parse_csv('v\n""\n\n')
    with pytest.raises(ValueError):
        column_stats(rows, "v")


def test_floats_and_negatives():
    rows = parse_csv("v\n-1.5\n2.5\n")
    s = column_stats(rows, "v")
    assert s["min"] == -1.5 and s["max"] == 2.5 and s["avg"] == 0.5
