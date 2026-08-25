def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group anagrams together.

    - Groups appear in order of their first member's first occurrence.
    - Within each group, words keep their original relative order.
    """
    groups: dict = {}
    for w in words:
        key = frozenset(w)
        groups.setdefault(key, []).append(w)
    return list(groups.values())
