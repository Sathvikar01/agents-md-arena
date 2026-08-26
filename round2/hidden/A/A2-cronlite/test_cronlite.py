import pytest
from datetime import datetime

from cronlite import next_after


def test_every_minute():
    assert next_after("* * * * *", datetime(2026, 1, 1, 0, 0)) == datetime(2026, 1, 1, 0, 1)


def test_daily_at_1430():
    e = "30 14 * * *"
    assert next_after(e, datetime(2026, 3, 1, 13, 0)) == datetime(2026, 3, 1, 14, 30)
    assert next_after(e, datetime(2026, 3, 1, 14, 30)) == datetime(2026, 3, 2, 14, 30)


def test_strictly_after_same_minute():
    assert next_after("*/10 * * * *", datetime(2026, 5, 5, 5, 20)) == datetime(2026, 5, 5, 5, 30)


def test_list_and_range():
    assert next_after("5,35 9-10 * * *", datetime(2026, 7, 7, 9, 40)) == datetime(2026, 7, 7, 10, 5)
    assert next_after("0 22 1-5 * *", datetime(2026, 7, 4, 23, 0)) == datetime(2026, 7, 5, 22, 0)


def test_step():
    assert next_after("*/15 * * * *", datetime(2026, 1, 1, 0, 16)) == datetime(2026, 1, 1, 0, 30)
    assert next_after("0 0-23/6 * * *", datetime(2026, 1, 1, 6, 0, 1)) == datetime(2026, 1, 1, 12, 0)


def test_dow_only_sunday_is_zero():
    # Sunday 2026-08-30
    assert next_after("0 12 * * 0", datetime(2026, 8, 24, 0, 0)) == datetime(2026, 8, 30, 12, 0)
    # Monday 2026-08-31
    assert next_after("59 23 * * 1", datetime(2026, 8, 24, 0, 0)) == datetime(2026, 8, 24, 23, 59)


def test_dom_only_skips_missing_dates():
    assert next_after("0 0 31 * *", datetime(2026, 4, 1, 0, 0)) == datetime(2026, 5, 31, 0, 0)


def test_leap_year_feb29():
    assert next_after("0 0 29 2 *", datetime(2026, 1, 1, 0, 0)) == datetime(2028, 2, 29, 0, 0)


def test_vixie_or_rule_both_restricted():
    # Fri 2026-08-28; dom=13 restricted, dow=5(Fri) restricted -> either matches
    e = "0 0 13 * 5"
    # next match: Fri 2026-08-28 (dow), NOT waiting for the 13th
    assert next_after(e, datetime(2026, 8, 27, 12, 0)) == datetime(2026, 8, 28, 0, 0)
    # then Thu Aug 13 2027? No: next Fri-the-13th or any Friday: Friday Sep 4 2026
    assert next_after(e, datetime(2026, 8, 28, 0, 0)) == datetime(2026, 9, 4, 0, 0)


def test_month_boundary_year_roll():
    assert next_after("0 0 1 1 *", datetime(2026, 12, 31, 12, 0)) == datetime(2027, 1, 1, 0, 0)


@pytest.mark.parametrize("bad", [
    "", "* * * *", "60 * * * *", "* 24 * * *", "* * 32 * *",
    "* * * 13 *", "* * * * 7", "MON * * * *", "a * * * *",
])
def test_invalid_expressions(bad):
    with pytest.raises(ValueError):
        next_after(bad, datetime(2026, 1, 1))
