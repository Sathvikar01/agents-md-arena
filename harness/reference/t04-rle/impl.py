def encode(s: str) -> str:
    if not s:
        return ""
    result = []
    count = 1
    prev = s[0]
    for cur in s[1:]:
        if cur == prev:
            count += 1
        else:
            result.append(f"{prev}{count}")
            count = 1
            prev = cur
    result.append(f"{prev}{count}")
    return "".join(result)


import re


def decode(s: str) -> str:
    return "".join(
        ch * int(n) for ch, n in re.findall(r"(\D)(\d+)", s)
    )
