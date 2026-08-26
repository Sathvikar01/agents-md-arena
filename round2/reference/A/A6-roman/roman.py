_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
_SUBS = {"IV": 4, "IX": 9, "XL": 40, "XC": 90, "CD": 400, "CM": 900}
_MAX_REPEAT = {"I": 3, "X": 3, "C": 3, "M": 3, "V": 1, "L": 1, "D": 1}


def to_int(s) -> int:
    if not isinstance(s, str) or s == "":
        raise ValueError("empty or non-string")
    if any(ch not in _VALUES for ch in s):
        raise ValueError(f"illegal characters in {s!r}")
    i = 0
    total = 0
    prev_token_val = None   # numeric value of the previous token
    prev_char = None        # for repeat tracking (singles only)
    run_len = 0
    while i < len(s):
        two = s[i:i + 2]
        if len(two) == 2 and two in _SUBS:
            if prev_token_val is not None and prev_token_val < _VALUES[two[1]]:
                raise ValueError(f"non-canonical order around {two}")
            total += _SUBS[two]
            prev_token_val = _SUBS[two]
            prev_char, run_len = None, 0
            i += 2
        else:
            ch = s[i]
            if ch == prev_char:
                run_len += 1
            else:
                prev_char, run_len = ch, 1
            if run_len > _MAX_REPEAT[ch]:
                raise ValueError(f"too many {ch} repeats")
            # a single may not be followed by a larger single (must use pairs)
            nxt = s[i + 1] if i + 1 < len(s) else ""
            if nxt and _VALUES[nxt] > _VALUES[ch]:
                raise ValueError(f"invalid descending order near {ch}{nxt}")
            total += _VALUES[ch]
            prev_token_val = _VALUES[ch]
            i += 1
    return total


def from_int(n) -> str:
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be int")
    if n < 1 or n > 3999:
        raise ValueError("out of range")
    parts = (
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    )
    out = []
    rem = n
    for val, sym in parts:
        cnt, rem = divmod(rem, val)
        out.append(sym * cnt)
    return "".join(out)
