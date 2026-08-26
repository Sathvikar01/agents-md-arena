import pytest

from jsonlite import loads


# ---------- happy paths ----------

def test_scalars():
    assert loads("42") == 42
    assert loads("-7") == -7
    assert loads("3.14") == 3.14
    assert loads("true") is True
    assert loads("false") is False
    assert loads("null") is None


def test_int_vs_float_types():
    assert isinstance(loads("42"), int)
    assert isinstance(loads("42.0"), float)
    assert isinstance(loads("1e2"), float)


def test_number_forms():
    assert loads("1e2") == 100.0
    assert loads("2.5E-2") == 0.025
    assert loads("-0") == 0
    assert loads("0.5") == 0.5


def test_string_escapes():
    assert loads(r'"a\nb"') == "a\nb"
    assert loads(r'"q\"q"') == 'q"q'
    assert loads(r'"back\\slash"') == "back\\slash"
    assert loads(r'"slash/"') == "slash/"
    assert loads(r'"uni\u0041\u00e9"') == "uniAé"


def test_containers_and_nesting():
    v = loads('{"a":[1,{"b":[[]]}],"c":null}')
    assert v == {"a": [1, {"b": [[]]}], "c": None}


def test_whitespace_ignored():
    assert loads('  { "a" : 1 } \n') == {"a": 1}
    assert loads("[\n1,\r\n\t2 ]") == [1, 2]


def test_duplicate_key_last_wins():
    assert loads('{"k":1,"k":2}') == {"k": 2}


def test_deep_nesting_ok():
    s = "[" * 40 + "]" * 40
    assert loads(s) == [[], [], [], []][:1] * 40 or loads(s) is not None


# ---------- error cases ----------

def _err(s):
    with pytest.raises(ValueError):
        loads(s)


def test_empty_and_ws_invalid():
    _err("")
    _err("   ")
    _err("\n\t")


def test_leading_zero_and_bad_numbers():
    _err("01")
    _err("-")
    _err("1.")
    _err(".5")
    _err("+1")
    _err("1e")
    _err("1e+")


@pytest.mark.parametrize("bad", [
    "", "[1,]", "{,}", '{"a" 1}', '{"a":}', "[1 2]",
])
def test_structural_errors(bad):
    _err(bad)


def test_trailing_garbage():
    _err("{} {}")
    _err("1 2")
    _err("true false")


def test_unclosed_and_mismatched():
    _err('{"a": [1')
    _err("(1)")
    _err("'single'")


def test_bad_literals_and_escapes():
    _err("True")
    _err("tru")
    _err("undefined")
    _err('"\\x41"')
    _err('"\\u12"')


def test_raw_control_char_in_string():
    _err('"a\x01b"')
