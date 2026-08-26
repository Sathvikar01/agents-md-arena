import pytest

from tokenbucket import TokenBucket


class ScriptClock:
    def __init__(self, start=0.0):
        self.t = float(start)


def make(rate=2.0, cap=3.0, start=0.0):
    ck = ScriptClock(start)
    return TokenBucket(rate, cap, clock=lambda: ck.t), ck


def test_invalid_args():
    with pytest.raises(ValueError):
        TokenBucket(0, 5, clock=ScriptClock)
    with pytest.raises(ValueError):
        make(cap=0)


def test_starts_full():
    b, _ = make(cap=3)
    assert b.available() == 3.0


def test_drain_then_refill_linear():
    b, ck = make(rate=2.0, cap=3.0)
    assert b.try_consume(3) is True
    assert b.available() == 0.0
    ck.t = 0.5                       # +1.0 tokens
    assert b.available() == 1.0
    assert b.try_consume(1) is True
    assert b.available() == 0.0


def test_clamped_at_capacity():
    b, ck = make(rate=2.0, cap=3.0)
    ck.t = 100.0
    assert b.available() == 3.0


def test_failed_consume_keeps_state():
    b, ck = make()
    assert b.try_consume(3) is True
    ck.t = 0.25                      # 0.5 tokens available
    assert b.try_consume(1) is False
    assert b.available() == pytest.approx(0.5)


def test_fractional_refill_exact():
    b, ck = make(rate=10.0, cap=10.0)
    b.try_consume(10)
    ck.t = 0.333                     # 3.33 tokens
    assert b.available() == pytest.approx(3.33)


def test_n_above_capacity_never_succeeds():
    b, ck = make(rate=2.0, cap=3.0)
    assert b.try_consume(4) is False
    ck.t = 50.0
    assert b.try_consume(4) is False


def test_negative_n_invalid():
    b, _ = make()
    with pytest.raises(ValueError):
        b.try_consume(-1)


def test_zero_n_succeeds_even_when_empty():
    b, _ = make()
    b.try_consume(3)
    assert b.try_consume(0) is True


def test_burst_pattern():
    b, ck = make(rate=1.0, cap=2.0)
    assert b.try_consume(2) is True
    ck.t = 1.0
    assert b.try_consume(1) is True   # refilled exactly 1
    ck.t = 1.5
    assert b.try_consume(1) is False  # only 0.5 accumulated
    ck.t = 2.0
    assert b.try_consume(1) is True


def test_rate_zero_rejected_explicitly():
    with pytest.raises(ValueError):
        TokenBucket(0.0, 1.0, clock=ScriptClock())
