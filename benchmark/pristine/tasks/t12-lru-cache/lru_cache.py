from collections import OrderedDict


class LRUCache:
    """Fixed-capacity least-recently-used cache.

    - get(key): return value or None on miss; a hit counts as use.
    - put(key, value): insert/update; evicts the least recently used entry
      when capacity is exceeded.
    """

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self._data: OrderedDict = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return None
        return self._data[key]

    def put(self, key, value) -> None:
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)
