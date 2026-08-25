from impl import is_balanced


def test_simple_pairs():
    assert is_balanced("()") is True
    assert is_balanced("[]") is True
    assert is_balanced("{}") is True


def test_nested_mixed():
    assert is_balanced("{[()]}") is True
    assert is_balanced("()[]{}") is True


def test_unclosed_open():
    assert is_balanced("((") is False
    assert is_balanced("({[}") is False


def test_wrong_order():
    assert is_balanced("([)]") is False


def test_close_before_open():
    assert is_balanced(")(") is False


def test_empty():
    assert is_balanced("") is True


def test_other_chars_ignored():
    assert is_balanced("def f(x): return d[k] + (a-b)") is True


def test_extra_closer():
    assert is_balanced("() }") is False
