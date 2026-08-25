import pytest
from impl import is_prime, nth_prime


@pytest.mark.parametrize(
    "m,expected",
    [
        (2, True),
        (3, True),
        (4, False),
        (9, False),
        (25, False),
        (29, True),
        (97, True),
        (91, False),  # 7*13
    ],
)
def test_is_prime(m, expected):
    assert is_prime(m) is expected


def test_first_primes():
    assert [nth_prime(i) for i in range(1, 6)] == [2, 3, 5, 7, 11]


def test_tenth():
    assert nth_prime(10) == 29


def test_hundredth():
    assert nth_prime(100) == 541


def test_invalid():
    with pytest.raises(ValueError):
        nth_prime(0)
