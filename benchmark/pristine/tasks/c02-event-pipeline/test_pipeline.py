from events import Event
from window import filter_by_window, in_window
from buckets import count_per_bucket, count_by_kind_per_bucket, bucket_start
from pipeline import process


def ev(ts):
    return Event(ts=ts, kind="click")


# ---------- window ----------

def test_start_inclusive():
    assert in_window(ev(10), 10, 20) is True


def test_end_exclusive():
    assert in_window(ev(20), 10, 20) is False
    assert in_window(ev(19), 10, 20) is True


def test_filter_preserves_order():
    events = [ev(15), ev(5), ev(25), ev(12)]
    got = [e.ts for e in filter_by_window(events, 10, 20)]
    assert got == [15, 12]


# ---------- buckets ----------

def test_bucket_start_aligns_to_minute():
    assert bucket_start(0) == 0
    assert bucket_start(59) == 0
    assert bucket_start(60) == 60
    assert bucket_start(119) == 60
    assert bucket_start(3661) == 3660


def test_count_per_bucket():
    events = [ev(0), ev(30), ev(59), ev(61), ev(130)]
    counts = count_per_bucket(events)
    assert counts == {0: 3, 60: 1, 120: 1}


def test_kind_filter():
    events = [
        Event(ts=10, kind="click"),
        Event(ts=15, kind="signup"),
        Event(ts=20, kind="click"),
    ]
    assert count_by_kind_per_bucket(events, "signup") == {0: 1}


# ---------- pipeline integration ----------

def test_process_integration():
    events = [ev(t) for t in (65, 100, 119, 120, 200)]
    out = process(events, start=60, end=120)
    assert out["total"] == 3
    assert out["per_minute"] == {60: 3}


def test_process_empty_window():
    assert process([ev(50)], start=100, end=110) == {"total": 0, "per_minute": {}}
