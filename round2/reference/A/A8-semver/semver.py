import re
from dataclasses import dataclass
from typing import Optional, Tuple

_CORE = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
_PRE = r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
_BUILD = r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
_FULL_RE = re.compile(rf"^{_CORE}{_PRE}{_BUILD}$")


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int
    prerelease: Tuple[str, ...] = ()
    build: Optional[str] = None

    @property
    def triple(self):
        return (self.major, self.minor, self.patch)

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return cmp_versions(self, other) == 0

    def __lt__(self, other):
        return cmp_versions(self, other) < 0

    def __le__(self, other):
        return cmp_versions(self, other) <= 0

    def __gt__(self, other):
        return cmp_versions(self, other) > 0

    def __ge__(self, other):
        return cmp_versions(self, other) >= 0

    def __hash__(self):
        return hash((self.major, self.minor, self.patch, self.prerelease))


def parse_version(s: str) -> Version:
    if not isinstance(s, str):
        raise ValueError("version must be str")
    m = _FULL_RE.match(s.strip())
    if not m:
        raise ValueError(f"malformed version {s!r}")
    major, minor, patch, pre, build = m.groups()
    pre_ids: Tuple[str, ...] = ()
    if pre is not None:
        for ident in pre.split("."):
            if ident.isdigit() and len(ident) > 1 and ident[0] == "0":
                raise ValueError("numeric prerelease id with leading zero")
        pre_ids = tuple(pre.split("."))
    return Version(int(major), int(minor), int(patch), pre_ids, build)


def _pre_key(v: Version):
    if not v.prerelease:
        return None
    return tuple(
        (0, int(x), "") if x.isdigit() else (1, 0, x) for x in v.prerelease
    )


def cmp_versions(a: Version, b: Version) -> int:
    ka, kb = _pre_key(a), _pre_key(b)
    if a.triple != b.triple:
        return -1 if a.triple < b.triple else 1
    if ka == kb:
        return 0
    if ka is None:
        return 1
    if kb is None:
        return -1
    return -1 if ka < kb else 1


def _parse_partial(s: str):
    """Zero-fill / wildcard interpretation of a comparator body."""
    s = s.strip()
    if s in ("", "*", "x", "X"):
        return Version(0, 0, 0), None            # base, upper-triple|None
    pre = ""
    if "-" in s:
        s, _, pre = s.partition("-")
    nums = s.split(".")
    while nums and nums[-1] in ("x", "X", "*"):
        nums.pop()
    if len(nums) == 0:
        return Version(0, 0, 0), None
    if len(nums) == 1:
        n = int(nums[0])
        return Version(n, 0, 0), (n + 1, 0, 0)
    if len(nums) == 2:
        a, b = int(nums[0]), int(nums[1])
        return Version(a, b, 0), (a, b + 1, 0)
    v = parse_version(".".join(nums) + (f"-{pre}" if pre else ""))
    return v, None


class _Comp:
    def __init__(self, raw: str):
        self.raw = raw.strip()
        body = self.raw
        self.op = "="
        for op in (">=", "<=", ">", "<", "=", "^", "~"):
            if body.startswith(op):
                self.op, body = op, body[len(op):]
                break
        self.is_any = body.strip() in ("", "*", "x", "X")
        self.base, self.wild_hi = None, None
        if not self.is_any:
            pre = ""
            core_body = body
            if "-" in core_body:
                core_body, _, pre = core_body.partition("-")
            nums = core_body.split(".")
            while nums and nums[-1] in ("x", "X", "*"):
                nums.pop()
            if self.op in ("=", "^", "~"):
                # partials behave as x-ranges here
                if len(nums) == 0:
                    self.base, self.wild_hi = Version(0, 0, 0), None
                elif len(nums) == 1:
                    n = int(nums[0])
                    self.base, self.wild_hi = Version(n, 0, 0), (n + 1, 0, 0)
                elif len(nums) == 2:
                    a, b = int(nums[0]), int(nums[1])
                    self.base, self.wild_hi = Version(a, b, 0), (a, b + 1, 0)
                else:
                    s_full = ".".join(nums) + (f"-{pre}" if pre else "")
                    self.base, self.wild_hi = parse_version(s_full), None
            else:
                while len(nums) < 3:
                    nums.append("0")
                s_full = ".".join(nums) + (f"-{pre}" if pre else "")
                self.base = parse_version(s_full)

    def bounds(self):
        """(low_inclusive Version|None, high_exclusive triple|None)."""
        if self.is_any:
            return Version(0, 0, 0), None
        v, whi = self.base, self.wild_hi
        if self.op == ">=":
            return v, None
        if self.op == ">":
            return Version(v.major, v.minor, v.patch + 1), None
        if self.op == "<":
            return None, v.triple
        if self.op == "<=":
            return None, (v.major, v.minor, v.patch + 1)
        if self.op == "^":
            if v.major > 0:
                return v, (v.major + 1, 0, 0)
            if v.minor > 0:
                return v, (0, v.minor + 1, 0)
            return v, (0, 0, v.patch + 1)
        if self.op == "~":
            return v, (v.major, v.minor + 1, 0)
        # '=' / bare / x-range: half-open [base, upper)
        if whi is not None:
            return v, whi
        return v, (v.major, v.minor, v.patch + 1)


def satisfies(version_str: str, range_str: str) -> bool:
    ver = parse_version(version_str)
    comps = [_Comp(t) for t in re.split(r"[ ,]+", range_str.strip()) if t]
    if not comps:
        comps = [_Comp("*")]
    for c in comps:
        lo, hi = c.bounds()
        if lo is not None and cmp_versions(ver, lo) < 0:
            return False
        if hi is not None and ver.triple >= hi:
            return False
    if ver.prerelease:
        gated = any(
            c.base is not None and c.base.prerelease and c.base.triple == ver.triple
            for c in comps
        )
        if not gated:
            return False
    return True
