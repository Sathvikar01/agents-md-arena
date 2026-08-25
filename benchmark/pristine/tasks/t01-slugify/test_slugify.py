from slugify import slugify


def test_basic():
    assert slugify("Hello World") == "hello-world"


def test_collapses_spaces_and_punctuation():
    assert slugify("  Multiple   Spaces,  Here! ") == "multiple-spaces-here"


def test_symbols_collapse_to_one_hyphen():
    assert slugify("C++ & C#") == "c-c"


def test_strips_leading_trailing():
    assert slugify("--leading and trailing--") == "leading-and-trailing"


def test_numbers_kept():
    assert slugify("Python 3.12 Rocks") == "python-3-12-rocks"


def test_empty():
    assert slugify("") == ""


def test_only_punctuation():
    assert slugify("!!! ???") == ""


def test_already_clean():
    assert slugify("clean-string-42") == "clean-string-42"
