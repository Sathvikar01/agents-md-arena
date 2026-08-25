import re


def slugify(title: str) -> str:
    """Convert a title into a URL slug.

    Rules:
      - lowercase everything
      - every run of non-alphanumeric characters becomes a single hyphen
      - leading/trailing hyphens are stripped
    """
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s
