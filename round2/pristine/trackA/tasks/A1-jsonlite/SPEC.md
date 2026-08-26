# Task: jsonlite

Implement `loads(text: str)` in `jsonlite.py`.

**The full binding contract is the module docstring inside `jsonlite.py`.**
Grading uses hidden exhaustive tests written from that docstring. Highlights:

- Recursive JSON values: objects, arrays, strings, numbers, true/false/null
- Strict RFC 8259 subset behavior: NO trailing commas, NO comments,
  NO leading zeros (`01` invalid), NO trailing garbage after the value
- Escapes: `\" \\ \/ \b \f \n \r \t \uXXXX`
- Invalid input must raise `ValueError` (never return a wrong value)
- Duplicate object keys: last occurrence wins
- Top-level scalar values are legal (`"42"`, `"true"`, `"null"`)

Edge checklist (not exhaustive — read the docstring):
empty input, whitespace-only, unclosed containers, `1.` / `.5` / `+1`,
raw control characters inside strings, `\u` escapes, deeply nested arrays.
