def encode(s: str) -> str:
    """Run-length encode: "aaabbc" -> "a3b2c1"."""
    if not s:
        return ""
    result = []
    count = 1
    for prev, cur in zip(s, s[1:]):
        if cur == prev:
            count += 1
        else:
            result.append(f"{prev}{count}")
            count = 1
    return "".join(result)


def decode(s: str) -> str:
    """Inverse of encode: "a3b2c1" -> "aaabbc". Counts may be multi-digit."""
    out = []
    num = ""
    for ch in s:
        if ch.isdigit():
            num += ch
        else:
            out.append(ch * int(num))
            num = ""
    return "".join(out)
