"""Token bucket rate limiter.

Contract — implement class TokenBucket exactly as specified:

    TokenBucket(rate_per_sec: float, capacity: float, clock=None)

Semantics:
    - rate_per_sec > 0 and capacity > 0 are required, else ValueError.
    - clock: zero-arg callable returning float seconds; default time.time.
      ALL timing uses this clock only.
    - The bucket starts FULL: tokens == capacity at construction.
    - Refill is CONTINUOUS: at any moment,
          tokens = min(capacity, tokens_prev + elapsed * rate_per_sec)
      computed lazily from the last mutation time.
    - available(): current token count as float (after applying refill).
    - try_consume(n=1): if n < 0 -> ValueError. If current tokens >= n
      (after refill), deduct n and return True; otherwise return False and
      leave state unchanged EXCEPT the lazy refill still applies.
    - n may exceed capacity: then try_consume can never succeed (tokens are
      capped at capacity) -> False always.
    - Floating point: comparisons use exact floats; do not round.

Example:
    t = [0.0]
    b = TokenBucket(rate_per_sec=2.0, capacity=3.0, clock=lambda: t[0])
    assert b.try_consume(3) is True       # full bucket
    assert b.try_consume(1) is False      # empty
    t[0] = 0.5                            # 1 second? no: 0.5s * 2/s = 1 token
    assert b.available() == 1.0
    assert b.try_consume(1) is True
    t[0] = 10.0                           # long wait -> clamped to capacity
    assert b.available() == 3.0
"""


class TokenBucket:
    def __init__(self, rate_per_sec: float, capacity: float, clock=None):
        raise NotImplementedError

    def available(self) -> float:
        raise NotImplementedError

    def try_consume(self, n: float = 1) -> bool:
        raise NotImplementedError
