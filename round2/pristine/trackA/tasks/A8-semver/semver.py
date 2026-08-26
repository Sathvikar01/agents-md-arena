"""Semantic Versioning 2.0.0 utilities.

Contract — implement exactly:

parse_version(s: str) -> Version
    Version objects expose .major .minor .patch (ints), .prerelease
    (tuple of identifier strings, possibly empty) and .build (str or None).
    Format: major.minor.patch[-prerelease][+build]
      - major/minor/patch are digits WITHOUT leading zeros ('01' invalid)
      - prerelease is dot-separated identifiers: alphanumerics+hyphen,
        non-empty; numeric identifiers must not have leading zeros
      - build metadata follows '+', non-empty, no semantic meaning
    Malformed input raises ValueError.

Ordering (SemVer 2.0.0):
    major, then minor, then patch numerically; then a version WITHOUT
    prerelease > any with; prerelease identifiers compare left to right:
    numeric < alphanumeric; numeric compared numerically; alphanumeric by
    ASCII; a shorter list sorts before a longer one when it is a prefix.
    Build metadata is IGNORED in comparisons (equality includes it being
    ignored too).

satisfies(version_str: str, range_str: str) -> bool
    range_str = comparators separated by spaces and/or commas; ALL must hold.
    Comparators:
        >=V   >V   <=V   <V   =V     (V = full or partial version)
        ^V    up to next breaking release:
                ^1.2.3 -> [1.2.3, 2.0.0); ^0.2.3 -> [0.2.3, 0.3.0);
                ^0.0.3 -> [0.0.3, 0.0.4)
        ~V    same minor: ~1.2.3 -> [1.2.3, 1.3.0); ~1.2 -> [1.2.0, 1.3.0)
        X-ranges: '*' any; '1.x'/'1' -> [1.0.0, 2.0.0);
                  '1.2.x'/'1.2' -> [1.2.0, 1.3.0)
        A bare full version '1.2.3' means '=1.2.3'.
        Partial versions in relational comparators are zero-filled
        ('>=1.2' == '>=1.2.0').
    Prerelease gate: a version WITH a prerelease tag satisfies the range
    ONLY IF at least one comparator carries an explicit prerelease whose
    (major,minor,patch) triple equals the candidate's triple.
      e.g. satisfies('1.3.0-beta','>=1.2.0')          -> False
           satisfies('1.3.0-beta','>=1.3.0-alpha')    -> True
           satisfies('1.4.0-beta','>=1.3.0-alpha')    -> False

Examples:
    parse_version('1.2.3-rc.1+exp').prerelease == ('rc','1')
    satisfies('2.0.0', '^1.2.3') is False
    satisfies('1.9.9', '~1.2')   is False
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int
    prerelease: Tuple[str, ...] = ()
    build: Optional[str] = None


def parse_version(s: str) -> Version:
    raise NotImplementedError


def satisfies(version_str: str, range_str: str) -> bool:
    raise NotImplementedError
