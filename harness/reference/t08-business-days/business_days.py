from datetime import date, timedelta


def business_days(start: date, end: date) -> int:
    days = 0
    cur = start
    while cur < end:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return days
