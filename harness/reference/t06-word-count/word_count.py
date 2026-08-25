import re
from collections import Counter


def top_words(text: str, k: int) -> list[tuple[str, int]]:
    words = re.findall(r"[A-Za-z0-9']+", text)
    counts = Counter(w.lower() for w in words)
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:k]
