from datetime import date, timedelta


def business_days(start: date, end: date) -> int:
    """Count business days (Mon-Fri) from start inclusive to end exclusive.

    Returns 0 if end <= start.
    """
    days = 0
    cur = start
    while cur < end:
        if cur.weekday() < 6:
            days += 1
        cur += timedelta(days=1)
    return days
