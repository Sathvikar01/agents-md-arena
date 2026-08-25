import re


def compile_pattern(pattern: str) -> "re.Pattern":
    parts = []
    for seg in pattern.strip("/").split("/"):
        if seg.startswith(":"):
            name = seg[1:]
            parts.append(f"(?P<{name}>[^/]+)")
        else:
            parts.append(re.escape(seg))
    return re.compile("^/" + "/".join(parts) + "$")


def match(pattern: str, path: str) -> dict | None:
    m = compile_pattern(pattern).match(path)
    return m.groupdict() if m else None
