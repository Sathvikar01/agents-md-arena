import pytest

from roman import to_int, from_int


@pytest.mark.parametrize("s,n", [
    ("I", 1), ("III", 3), ("IV", 4), ("IX", 9),
    ("XL", 40), ("XC", 90), ("CD", 400), ("CM", 900),
    ("MCMXCIV", 1994), ("MMXXVI", 2026), ("MMMCMXCIX", 3999),
    ("LVIII", 58), ("DCCCXLV", 845),
])
def test_to_int(s, n):
    assert to_int(s) == n


@pytest.mark.parametrize("n,s", [
    (1, "I"), (4, "IV"), (9, "IX"), (14, "XIV"), (40, "XL"), (90, "XC"),
    (400, "CD"), (900, "CM"), (1994, "MCMXCIV"), (2026, "MMXXVI"),
    (3999, "MMMCMXCIX"), (3888, "MMMDCCCLXXXVIII"),
])
def test_from_int(n, s):
    assert from_int(n) == s


def test_roundtrip_range():
    for n in list(range(1, 150)) + [500, 999, 1234, 2999, 3999]:
        assert to_int(from_int(n)) == n


@pytest.mark.parametrize("bad", [
    "", "ii", "xiv", "ABC", "IIII", "VV", "IC", "IL", "XM", "VX",
    "LC", "DM", "IIV", "XXXX", "MMMM",
])
def test_malformed_raise(bad):
    with pytest.raises(ValueError):
        to_int(bad)


@pytest.mark.parametrize("bad_n", [0, -5, 4000, 10000])
def test_out_of_range(bad_n):
    with pytest.raises(ValueError):
        from_int(bad_n)


def test_non_int_rejected():
    with pytest.raises(ValueError):
        from_int("10")  # type: ignore[arg-type]
