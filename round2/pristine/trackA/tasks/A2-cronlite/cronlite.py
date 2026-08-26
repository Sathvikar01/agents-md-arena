"""Minimal cron expression evaluator.

Contract — implement next_after(expr, after) exactly as specified:

next_after(expr: str, after: datetime.datetime) -> datetime.datetime

expr has FIVE fields separated by whitespace:
    minute  hour  day-of-month  month  day-of-week

Field syntax (each field independently):
    '*'          any allowed value
    'a'          single value
    'a-b'        inclusive range
    'a-b/s'      range with step s (values a, a+s, ... <= b)
    '*/s'        full range with step s
    'a,b,c'      comma-separated list of any of the above
Allowed ranges:
    minute 0-59, hour 0-23, day-of-month 1-31, month 1-12,
    day-of-week 0-6 where 0=SUNDAY, 1=Monday ... 6=Saturday.
    Values outside the allowed range are ValueError. Names (MON, JAN) are
    NOT supported -> ValueError. Empty expr / wrong field count -> ValueError.

Semantics:
    - A datetime matches if every field value is allowed AND the vixie-cron
      day rule holds: if BOTH day-of-month and day-of-week are restricted
      (i.e. not '*'), the day matches if EITHER dom or dow matches;
      otherwise the field must match normally.
    - The result is the earliest matching minute STRICTLY AFTER `after`
      (naive local time; no DST handling). If nothing matches within
      4 years from `after`, raise RuntimeError.
    - Malformed expressions raise ValueError.

Examples:
    next_after('* * * * *', datetime(2026,1,1,0,0))     == datetime(2026,1,1,0,1)
    next_after('30 14 * * *', datetime(2026,3,1,13,0))  == datetime(2026,3,1,14,30)
    next_after('30 14 * * *', datetime(2026,3,1,14,30)) == datetime(2026,3,2,14,30)
    next_after('0 0 29 2 *', datetime(2026,1,1,0,0))    == datetime(2028,2,29,0,0)  # leap year
"""


def next_after(expr: str, after):
    raise NotImplementedError
