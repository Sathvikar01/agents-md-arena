from rle import encode, decode


def test_encode_basic():
    assert encode("aaabbc") == "a3b2c1"


def test_encode_single_runs():
    assert encode("abcd") == "a1b1c1d1"


def test_encode_all_same():
    assert encode("aaaa") == "a4"
    assert encode("a") == "a1"


def test_encode_empty():
    assert encode("") == ""


def test_encode_repeats_after_break():
    assert encode("aabbaabb") == "a2b2a2b2"


def test_decode_basic():
    assert decode("a3b2c1") == "aaabbc"


def test_decode_multidigit():
    assert decode("a12") == "a" * 12


def test_roundtrip():
    for s in ["abc", "zzztttq", "m", "aabbaabb", "x" * 25]:
        assert decode(encode(s)) == s
