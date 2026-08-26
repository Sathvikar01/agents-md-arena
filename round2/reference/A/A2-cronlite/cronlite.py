from datetime import timedelta

_RANGES = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]


def _parse_field(field: str, lo: int, hi: int) -> set:
    vals = set()
    for part in field.split(","):
        if not part:
            raise ValueError("empty field element")
        step = 1
        body = part
        if "/" in part:
            body, _, step_s = part.partition("/")
            if not step_s.isdigit() or int(step_s) < 1 or "/" in body:
                raise ValueError("bad step")
            step = int(step_s)
        def parse_val(v):
            if not v.isdigit():
                raise ValueError(f"bad value {v!r}")
            n = int(v)
            if n < lo or n > hi:
                raise ValueError(f"value {n} out of range")
            return n
        if "-" in body:
            a, _, b = body.partition("-")
            start, end = parse_val(a), parse_val(b)
            if start > end:
                raise ValueError("inverted range")
            rng = range(start, end + 1)
        elif body == "*":
            rng = range(lo, hi + 1)
        else:
            v = parse_val(body)
            rng = range(v, hi + 1) if "/" in part else [v]
        vals.update(rng[::step])
    return vals


def next_after(expr: str, after):
    fields = expr.split()
    if len(fields) != 5:
        raise ValueError("expected 5 fields")
    minutes, hours, doms, months, dows = (
        _parse_field(f, lo, hi) for f, (lo, hi) in zip(fields, _RANGES))
    dom_r = fields[2] != "*"
    dow_r = fields[4] != "*"

    cur = after.replace(second=0, microsecond=0) + timedelta(minutes=1)
    limit = after + timedelta(days=366 * 4 + 1)
    while cur <= limit:
        day_ok = (
            (cur.day in doms or (cur.weekday() + 1) % 7 in dows)
            if (dom_r and dow_r)
            else (cur.day in doms and (cur.weekday() + 1) % 7 in dows)
        )
        if cur.minute in minutes and cur.hour in hours and cur.month in months and day_ok:
            return cur
        cur += timedelta(minutes=1)
    raise RuntimeError("no match within 4 years")
