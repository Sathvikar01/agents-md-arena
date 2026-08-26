# Task: cronlite

Implement `next_after(expr, after)` in `cronlite.py`. **The binding contract
is the module docstring inside `cronlite.py`** — hidden tests enforce it.

Quick checklist (see docstring for the authoritative version):

- 5 fields: minute hour day-of-month month day-of-week
- `*` , `,` `-` `/` syntax; step applies to ranges and `*`
- DOW: 0=Sun..6=Sat (7 is NOT accepted)
- Vixie-cron OR-rule when both DOM and DOW are restricted
- Result strictly after `after`, minute resolution, naive datetimes
