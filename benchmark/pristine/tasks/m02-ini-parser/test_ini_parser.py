import pytest
from ini_parser import parse_ini


def test_sections_and_keys():
    r = parse_ini("[a]\nx=1\n[b]\ny=2\n")
    assert r == {"a": {"x": "1"}, "b": {"y": "2"}}


def test_keys_before_any_section():
    assert parse_ini("root=on\n") == {"": {"root": "on"}}


def test_full_line_comments():
    r = parse_ini("# note\n;a also\n[k]\nv=1\n")
    assert r == {"k": {"v": "1"}}


def test_inline_comment_stripped():
    assert parse_ini("[s]\nport=8080 ; http\n") == {"s": {"port": "8080"}}


def test_empty_value_allowed():
    assert parse_ini("[s]\nflag=\n") == {"s": {"flag": ""}}


def test_duplicate_key_last_wins():
    assert parse_ini("[s]\nk=1\nk=2\n") == {"s": {"k": "2"}}


def test_whitespace_normalized():
    assert parse_ini("[s]\n   k   =   v   \n") == {"s": {"k": "v"}}


def test_value_with_equals_sign():
    assert parse_ini("[s]\nexpr=a==b\n") == {"s": {"expr": "a==b"}}


def test_blank_lines_ignored():
    assert parse_ini("\n[s]\n\nk=v\n\n") == {"s": {"k": "v"}}
