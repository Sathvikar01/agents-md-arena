"""Interval algebra over half-open intervals [low, high).

An interval is a tuple `(low, high)` with low < high; low/high may be int or
float. All functions are PURE (never mutate inputs). Invalid interval shape
(high <= low) raises ValueError wherever that interval is encountered as an
argument element or parameter.

Functions:

merge(ivs: list[tuple]) -> list[tuple]
    Normalize to a minimal sorted list of DISJOINT intervals covering the
    same total region. Touching intervals merge: [1,2) and [2,3) -> [1,3).
    Input order is arbitrary. Empty input -> [].

intersect(a: tuple, b: tuple) -> tuple | None
    Intersection of two half-open intervals; None if they do not overlap.
    [1,3) and [3,5) do NOT overlap (touching is empty for half-open).

hull(ivs: list[tuple]) -> tuple | None
    Minimal single interval containing everything; None for empty input.

gaps(ivs: list[tuple]) -> list[tuple]
    Holes strictly inside the hull, i.e. regions covered by NO interval but
    lying between the global min low and max high. Sorted ascending.

contains(iv: tuple, x) -> bool
    True iff low <= x < high.
"""

def merge(ivs):
    raise NotImplementedError


def intersect(a, b):
    raise NotImplementedError


def hull(ivs):
    raise NotImplementedError


def gaps(ivs):
    raise NotImplementedError


def contains(iv, x) -> bool:
    raise NotImplementedError
