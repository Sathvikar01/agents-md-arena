from collections import OrderedDict


class TTLCache:
    def __init__(self, capacity: int, ttl: float, clock=None):
        import time

        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.ttl = float(ttl)
        self._clock = clock or time.time
        self._data: OrderedDict = OrderedDict()  # key -> (value, expires_at)

    def _now(self):
        return self._clock()

    def put(self, key, value) -> None:
        now = self._now()
        self._purge_at(now)
        if key in self._data:
            del self._data[key]
        self._data[key] = (value, now + self.ttl)
        while len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def get(self, key):
        item = self._data.get(key)
        if item is None:
            return None
        value, expires_at = item
        if self._now() >= expires_at:
            return None
        self._data.move_to_end(key)
        return value

    def purge(self) -> int:
        return self._purge_at(self._now())

    def _purge_at(self, now: float) -> int:
        dead = [k for k, (_, exp) in self._data.items() if now >= exp]
        for k in dead:
            del self._data[k]
        return len(dead)

    def contains(self, key) -> bool:
        item = self._data.get(key)
        if item is None:
            return False
        return self._now() < item[1]

    def __len__(self) -> int:
        self._purge_at(self._now())
        return len(self._data)
