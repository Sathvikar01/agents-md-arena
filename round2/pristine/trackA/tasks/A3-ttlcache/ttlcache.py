"""LRU cache with per-entry TTL.

Contract — implement class TTLCache exactly as specified:

    TTLCache(capacity: int, ttl: float, clock: Callable[[], float] = time.time)

Semantics:
    - capacity must be >= 1 else ValueError.
    - ttl is the lifetime of an entry in seconds (float). ttl <= 0 means
      entries expire IMMEDIATELY (putting then getting returns None).
    - clock is a zero-argument callable returning the current time as float;
      all expiry math uses ONLY this clock (never time.time() directly),
      so tests can inject a scripted clock.
    - put(key, value): insert or update. Updates reset BOTH the value and
      the expiry timestamp AND mark the entry most-recently-used. If after
      insertion len(live entries) > capacity, evict least-recently-used
      live entries until within capacity. EXPIRED entries never occupy
      capacity: they are purged before the eviction decision.
    - get(key): return live value, or None if missing OR expired.
      A hit refreshes recency (moves to most-recently-used) but does NOT
      extend its expiry. A miss/expired-hit does not change any recency.
    - purge(): remove all expired entries, return the number removed.
    - __len__(): number of LIVE entries; expired entries are purged first,
      so len() always reflects non-expired contents.
    - contains(k): True iff k maps to a live (non-expired) value; must not
      change recency order.

Example:
    t = [1000.0]
    c = TTLCache(2, ttl=10.0, clock=lambda: t[0])
    c.put("a", 1); c.put("b", 2)
    t[0] = 1005.0
    c.get("a")          # -> 1, "a" now MRU
    c.put("c", 3)       # evicts "b" (LRU), NOT "a"
    assert c.get("b") is None and c.get("a") == 1
    t[0] = 1011.0       # everything expired (ttl=10)
    assert c.get("a") is None
"""


class TTLCache:
    def __init__(self, capacity: int, ttl: float, clock=None):
        raise NotImplementedError

    def put(self, key, value) -> None:
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def purge(self) -> int:
        raise NotImplementedError

    def contains(self, key) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
