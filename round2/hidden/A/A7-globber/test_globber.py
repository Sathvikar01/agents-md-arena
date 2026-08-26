import pytest

from globber import match


def test_literal_match():
    assert match("a/b/c", "a/b/c") is True
    assert match("a/b", "a/b/c") is False
    assert match("a/b/c", "a/b") is False


def test_star_within_segment():
    assert match("*.txt", "notes.txt") is True
    assert match("*", "") is True                      # zero chars allowed
    assert match("a*c", "abc") is True
    assert match("a*c", "abbc") is True
    assert match("a*c", "ac") is True
    assert match("a*c", "a/c") is False                # star can't cross sep
    assert match("*.py", "src/main.py") is False       # nor this one


def test_question_mark():
    assert match("a?c", "abc") is True
    assert match("a?c", "ac") is False
    assert match("a??", "abc") is True
    assert match("?", "/") is False                    # ? never matches sep


def test_doublestar_whole_segments():
    assert match("**", "a/b/c") is True
    assert match("**", "") is True
    assert match("a/**/b", "a/b") is True
    assert match("a/**/b", "a/x/y/b") is True
    assert match("**/*.md", "docs/deep/note.md") is True
    assert match("/**/*.md", "/docs/note.md") is True  # anchored form
    assert match("/**/*.md", "note.md") is False       # needs the empty head segment
    # '**' glued into a bigger segment loses magic:
    assert match("a**b", "axxb") is True               # treated as 'a*b' within segment
    assert match("a**b", "a/b") is False               # still can't cross sep


def test_empty_pattern_and_path():
    assert match("", "") is True
    assert match("", "a") is False
    assert match("a", "") is False


def test_trailing_separator_matters():
    assert match("a/", "a") is False
    assert match("a/", "a/") is True
    assert match("a", "a/") is False


def test_custom_separator():
    assert match("*.csv", "x.csv", sep=";") is True
    assert match("*.csv", "data;x.csv", sep=";") is False   # * cannot cross ';'
    assert match("a*", "a;b;c", sep=";") is False
    assert match("**", "x;y;z", sep=";") is True
