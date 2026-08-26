import pytest

from ttlcache import TTLCache


class FakeClock:
    def __init__(self, start=0.0):
        self.t = float(start)

    def __call__(self):
        return self.t

    def advance(self, dt):
        self.t += dt


def make(cap=2, ttl=10.0):
    ck = FakeClock()
    return TTLCache(cap, ttl, clock=ck), ck


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        TTLCache(0, 5.0, clock=FakeClock())


def test_put_get_roundtrip():
    c, _ = make()
    c.put("k", [1, 2])
    assert c.get("k") == [1, 2]


def test_missing_returns_none():
    c, _ = make()
    assert c.get("nope") is None


def test_expiry_by_clock():
    c, ck = make(ttl=5.0)
    c.put("x", 1)
    ck.advance(4.999)
    assert c.get("x") == 1
    ck.advance(0.002)
    assert c.get("x") is None


def test_zero_ttl_expires_immediately():
    c, _ = make(ttl=0.0)
    c.put("x", 1)
    assert c.get("x") is None


def test_put_resets_ttl():
    c, ck = make(ttl=10.0)
    c.put("x", 1)
    ck.advance(9.0)
    c.put("x", 2)          # resets both value and expiry window
    ck.advance(9.0)
    assert c.get("x") == 2
    ck.advance(1.1)
    assert c.get("x") is None


def test_evicts_lru_not_mru():
    c, _ = make(cap=2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.contains("b") and c.contains("c") and not c.contains("a")


def test_get_refreshes_recency_but_not_ttl():
    c, ck = make(cap=2, ttl=10.0)
    c.put("a", 1)
    c.put("b", 2)
    ck.advance(5)
    assert c.get("a") == 1           # a becomes MRU
    c.put("c", 3)                    # evicts b
    assert not c.contains("b")
    assert c.contains("a")
    ck.advance(6)                    # a was stored at t=0 -> expired regardless of hit
    assert c.get("a") is None


def test_expired_entries_do_not_count_for_capacity():
    c, ck = make(cap=2, ttl=10.0)
    c.put("a", 1)
    c.put("b", 2)
    ck.advance(11)                   # both expired
    c.put("c", 3)                    # purge happens; nothing evicted wrongly
    c.put("d", 4)                    # fits because a,b were dead
    assert sorted(k for k in ("c", "d") if c.contains(k)) == ["c", "d"]
    assert len(c) == 2


def test_purge_returns_count_and_cleans():
    c, ck = make(cap=5, ttl=10.0)
    c.put("a", 1)
    ck.advance(5)
    c.put("b", 2)
    ck.advance(6)                    # a expired (age 11), b alive (age 6)
    assert c.purge() == 1
    assert not c.contains("a") and c.contains("b")
    assert c.purge() == 0


def test_len_purges_expired_first():
    c, ck = make(cap=5, ttl=10.0)
    c.put("a", 1)
    ck.advance(5)
    c.put("b", 2)
    ck.advance(6)                    # a is now age 11 (expired), b age 6
    assert len(c) == 1


def test_contains_does_not_change_recency():
    c, _ = make(cap=2)
    c.put("a", 1)
    c.put("b", 2)
    c.contains("a")                  # peek: must NOT refresh recency
    c.put("c", 3)                    # still evicts a
    assert not c.contains("a")


def test_overwrite_updates_value_in_place():
    c, _ = make(cap=2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)                   # refresh recency too
    c.put("c", 3)
    assert c.get("a") == 10 and c.get("b") is None
