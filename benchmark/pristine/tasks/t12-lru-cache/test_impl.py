from impl import LRUCache


def test_put_and_get():
    c = LRUCache(2)
    c.put("a", 1)
    assert c.get("a") == 1


def test_miss_returns_none():
    c = LRUCache(2)
    assert c.get("missing") is None


def test_evicts_lru():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.get("a") is None
    assert c.get("b") == 2 and c.get("c") == 3


def test_get_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1  # now "b" is the LRU
    c.put("c", 3)
    assert c.get("b") is None
    assert c.get("a") == 1 and c.get("c") == 3


def test_update_existing_keeps_key():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)
    assert c.get("a") == 10
    assert c.get("b") is None


def test_capacity_one_churn():
    c = LRUCache(1)
    c.put("x", 1)
    c.put("y", 2)
    assert c.get("x") is None and c.get("y") == 2


def test_invalid_capacity():
    try:
        LRUCache(0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
