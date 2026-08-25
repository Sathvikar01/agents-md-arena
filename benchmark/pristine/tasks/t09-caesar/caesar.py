def shift(text: str, k: int) -> str:
    """Caesar-shift letters by k positions with wraparound.

    - lowercase stays lowercase, uppercase stays uppercase
    - non-letters pass through unchanged
    - negative k and k > 26 must work correctly
    """
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + k) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr(ord(ch) + k))
        else:
            out.append(ch)
    return "".join(out)
