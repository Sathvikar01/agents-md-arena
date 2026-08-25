from datetime import date
from impl import business_days

# Anchors: 2026-08-24 is a Monday, 2026-08-29 is a Saturday.


def test_one_full_week_mon_to_sat_exclusive():
    assert business_days(date(2026, 8, 24), date(2026, 8, 29)) == 5


def test_week_includes_no_weekend():
    assert business_days(date(2026, 8, 22), date(2026, 8, 24)) == 0  # Sat->Mon


def test_two_full_weeks():
    assert business_days(date(2026, 8, 24), date(2026, 9, 7)) == 10


def test_tuesday_to_next_tuesday():
    assert business_days(date(2026, 8, 25), date(2026, 9, 1)) == 5


def test_single_day_range():
    assert business_days(date(2026, 8, 25), date(2026, 8, 26)) == 1


def test_sunday_only():
    assert business_days(date(2026, 8, 30), date(2026, 8, 31)) == 0


def test_same_day():
    assert business_days(date(2026, 8, 25), date(2026, 8, 25)) == 0


def test_reversed_range():
    assert business_days(date(2026, 8, 26), date(2026, 8, 25)) == 0
