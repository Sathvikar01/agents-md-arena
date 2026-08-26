import pytest

from intervals import merge, intersect, hull, gaps, contains


# ---------- merge ----------

def test_merge_empty():
    assert merge([]) == []


def test_merge_unsorted_touching_and_overlap():
    assert merge([(5, 7), (1, 3), (2, 5)]) == [(1, 7)]


def test_merge_keeps_disjoint_sorted():
    assert merge([(10, 11), (0, 1)]) == [(0, 1), (10, 11)]


def test_merge_nested_absorbed():
    assert merge([(0, 10), (2, 3)]) == [(0, 10)]


def test_merge_float_touching():
    assert merge([(0.0, 0.5), (0.5, 1.0)]) == [(0.0, 1.0)]


def test_merge_invalid_interval_raises():
    with pytest.raises(ValueError):
        merge([(3, 3)])


# ---------- intersect ----------

def test_intersect_partial():
    assert intersect((1, 4), (3, 6)) == (3, 4)


def test_intersect_containment():
    assert intersect((0, 10), (2, 3)) == (2, 3)


def test_intersect_disjoint_none():
    assert intersect((1, 2), (5, 6)) is None


def test_intersect_touching_is_empty():
    assert intersect((1, 3), (3, 5)) is None


# ---------- hull ----------

def test_hull_basic_and_empty():
    assert hull([]) is None
    assert hull([(9, 10), (1, 2), (5, 6)]) == (1, 10)


# ---------- gaps ----------

def test_gaps_multiple_sorted():
    assert gaps([(0, 2), (3, 4), (6, 8), (1, 3)]) == [(4, 6)]


def test_gap_between_two():
    assert gaps([(0, 1), (2, 3)]) == [(1, 2)]


def test_no_gaps_when_covered():
    assert gaps([(0, 5), (2, 3)]) == []
    assert gaps([]) == []


# ---------- contains ----------

def test_contains_boundaries_half_open():
    assert contains((1, 5), 1) is True
    assert contains((1, 5), 5) is False
    assert contains((1, 5), 4.999) is True
    assert contains((1, 5), 0.999) is False
