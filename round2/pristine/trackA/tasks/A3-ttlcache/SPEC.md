# Task: ttlcache

Implement `TTLCache` in `ttlcache.py`. **Binding contract = module docstring.**

Key semantics hidden tests will enforce:
- lazy expiry via injected clock; LRU eviction only among live entries;
  `put` resets value+TTL+recency, `get` refreshes recency only
- `purge()` removes expired entries and returns how many it removed
