"""Route pattern matcher.

Pattern segments are split on "/". A segment starting with ":" captures
exactly one non-empty path segment into a named parameter. Other segments
must match literally. A pattern matches the WHOLE path or nothing.
"""

import re


def compile_pattern(pattern: str) -> "re.Pattern":
    parts = []
    for seg in pattern.strip("/").split("/"):
        if seg.startswith(":"):
            name = seg[1:]
            parts.append(f"(?P<{name}>.*)")
        else:
            parts.append(re.escape(seg))
    return re.compile("^/" + "/".join(parts) + "$")


def match(pattern: str, path: str) -> dict | None:
    """Return captured params dict if path matches pattern, else None."""
    m = compile_pattern(pattern).match(path)
    return m.groupdict() if m else None
