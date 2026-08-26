def match(pattern: str, path: str, sep: str = "/") -> bool:
    p_segs = pattern.split(sep)
    s_segs = path.split(sep)

    def seg_match(pat: str, seg: str) -> bool:
        i = j = 0
        star = -1
        mark_j = 0
        while j < len(seg):
            if i < len(pat) and (pat[i] == "?" or pat[i] == seg[j]):
                i += 1
                j += 1
            elif i < len(pat) and pat[i] == "*":
                star = i
                i += 1
                mark_j = j
            elif star != -1:
                i = star + 1
                j = mark_j + 1
                mark_j = j
            else:
                return False
        while i < len(pat) and pat[i] == "*":
            i += 1
        return i == len(pat)

    def seg_eq(pat: str, seg: str) -> bool:
        if "?" in pat or "*" in pat:
            return seg_match(pat, seg)
        return pat == seg

    n, m = len(p_segs), len(s_segs)
    seen = set()
    frontier = [(0, 0)]
    while frontier:
        pi, si = frontier.pop()
        if (pi, si) in seen:
            continue
        seen.add((pi, si))
        if pi == n:
            continue
        pat = p_segs[pi]
        if pat == "**":
            for skip in range(si, m + 1):
                nxt = (pi + 1, skip)
                if nxt not in seen:
                    frontier.append(nxt)
        elif si < m and seg_eq(pat, s_segs[si]):
            frontier.append((pi + 1, si + 1))
    return (n, m) in seen
