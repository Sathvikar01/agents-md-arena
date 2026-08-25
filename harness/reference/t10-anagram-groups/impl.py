def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict = {}
    for w in words:
        key = "".join(sorted(w))
        groups.setdefault(key, []).append(w)
    return list(groups.values())
