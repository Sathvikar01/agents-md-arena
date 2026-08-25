"""Minimal INI parser supporting:

- sections: [name]
- key=value pairs (value may be empty)
- full-line comments starting with # or ;
- inline comments: everything after " ;" or " #" outside of values is dropped
- keys before any section go to section ""
- duplicate keys: last one wins

parse_ini(text) -> dict[str, dict[str, str]]
"""
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
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        key, _, value = line.partition("=")
        result[section][key.strip()] = value.strip()
    return dict(result)
