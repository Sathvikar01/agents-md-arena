from collections import defaultdict


def parse_ini(text: str) -> dict[str, dict[str, str]]:
    result = defaultdict(dict)
    section = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line[0] in "#;":
            continue
        for marker in (" ;", " #", "\t;", "\t#"):
            idx = line.find(marker)
            if idx != -1:
                line = line[:idx].rstrip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        key, _, value = line.partition("=")
        result[section][key.strip()] = value.strip()
    return dict(result)
