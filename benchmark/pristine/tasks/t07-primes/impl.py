def is_prime(m: int) -> bool:
    """Primality check by trial division."""
    if m < 2:
        return False
    i = 2
    while i * i < m:
        if m % i == 0:
            return False
        i += 1
    return True


def nth_prime(n: int) -> int:
    """Return the n-th prime, 1-indexed (nth_prime(1) == 2)."""
    if n < 1:
        raise ValueError("n must be >= 1")
    count = 0
    candidate = 1
    while count < n:
        candidate += 1
        if is_prime(candidate):
            count += 1
    return candidate
