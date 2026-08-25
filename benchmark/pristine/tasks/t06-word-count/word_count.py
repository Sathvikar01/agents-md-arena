import re
from collections import Counter


def top_words(text: str, k: int) -> list[tuple[str, int]]:
    """Return the k most common words in text.

    - Words are sequences of letters, digits and apostrophes.
    - Matching is case-insensitive (report lowercase).
    - Ties are broken alphabetically ascending.
    - If fewer than k unique words exist, return all of them.
    """
    words = re.findall(r"[A-Za-z0-9']+", text)
    counts = Counter(w.lower() for w in words)
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return ranked[:k]
