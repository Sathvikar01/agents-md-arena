def _valid(iv):
    lo, hi = iv
    if not lo < hi:
        raise ValueError(f"invalid interval {iv!r}")
    return lo, hi


def merge(ivs):
    if not ivs:
        return []
    norm = sorted(_valid(iv) for iv in ivs)
    out = [norm[0]]
    for lo, hi in norm[1:]:
        clo, chi = out[-1]
        if lo <= chi:
            if hi > chi:
                out[-1] = (clo, hi)
        else:
            out.append((lo, hi))
    return out


def intersect(a, b):
    alo, ahi = _valid(a)
    blo, bhi = _valid(b)
    lo = max(alo, blo)
    hi = min(ahi, bhi)
    return (lo, hi) if lo < hi else None


def hull(ivs):
    if not ivs:
        return None
    norm = [_valid(iv) for iv in ivs]
    return (min(lo for lo, _ in norm), max(hi for _, hi in norm))


def gaps(ivs):
    m = merge(ivs)
    out = []
    for (lo, hi), (nlo, _) in zip(m, m[1:]):
        if nlo > hi:
            out.append((hi, nlo))
    return out


def contains(iv, x) -> bool:
    lo, hi = _valid(iv)
    return lo <= x < hi
