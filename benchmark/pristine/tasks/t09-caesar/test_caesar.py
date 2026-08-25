from caesar import shift


def test_lowercase_basic():
    assert shift("abc", 2) == "cde"


def test_lowercase_wraps():
    assert shift("xyz", 3) == "abc"


def test_uppercase_wraps():
    assert shift("XYZ", 3) == "ABC"


def test_preserves_case():
    assert shift("aBcZ", 1) == "bCdA"


def test_nonletters_unchanged():
    assert shift("Hello, World! 123", 5) == "Mjqqt, Btwqi! 123"


def test_negative_shift():
    assert shift("bcd", -1) == "abc"
    assert shift("A", -1) == "Z"


def test_shift_by_26_identity():
    assert shift("AbZx", 26) == "AbZx"


def test_large_shift():
    assert shift("abz", 53) == shift("abz", 1)
    assert shift("ABZ", 53) == shift("ABZ", 1)


def test_empty():
    assert shift("", 7) == ""
