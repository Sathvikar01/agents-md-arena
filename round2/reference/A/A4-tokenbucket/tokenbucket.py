import time


class TokenBucket:
    def __init__(self, rate_per_sec: float, capacity: float, clock=None):
        if rate_per_sec <= 0 or capacity <= 0:
            raise ValueError("rate_per_sec and capacity must be > 0")
        self.rate = float(rate_per_sec)
        self.capacity = float(capacity)
        self._clock = clock or time.time
        self._tokens = self.capacity
        self._last = self._clock()

    def available(self) -> float:
        now = self._clock()
        elapsed = now - self._last
        if elapsed > 0:
            self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
            self._last = now
        return self._tokens

    def try_consume(self, n: float = 1) -> bool:
        if n < 0:
            raise ValueError("n must be >= 0")
        if n > self.capacity:
            return False
        if self.available() >= n:
            self._tokens -= n
            self._last = self._clock()
            return True
        return False
