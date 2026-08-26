"""Strict minimal JSON parser (parse-only subset of RFC 8259).

Contract — implement loads(text) exactly as specified:

Return Python objects:
    JSON object  -> dict[str, Any]
    JSON array   -> list[Any]
    JSON string  -> str
    JSON number  -> int if integral literal without '.', 'e' or 'E';
                    float otherwise (including '1e2')
    true/false   -> True/False
    null         -> None

Grammar rules (violations raise ValueError):
    - text may be surrounded by insignificant whitespace (space, \\t, \\n, \\r)
      anywhere between tokens, but must contain exactly ONE top-level value;
      anything after it (except whitespace) is an error.
    - Empty or whitespace-only input is an error.
    - Strings are double-quoted. Allowed escapes:
        \" \\ \/ \b \f \n \r \t \uXXXX  (exactly four hex digits)
      Any other escape sequence is an error.
      A raw control character (code point < 0x20) inside a string is an error.
    - Numbers match:  -?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?
      So: leading zeros ('01'), lone '-' , '1.', '.5', '+1', '1e' are errors.
    - Objects: '{' (string ':' value) (',' string ':' value)* '}'
      Arrays:  '[' value (',' value)* ']'
      Trailing commas are errors. Missing colons/commas are errors.
    - Literals are exactly true, false, null (case sensitive; 'True' is an error)
    - Duplicate keys: the LAST value for a duplicated key wins.
    - Nesting depth: support at least 64 levels.

Examples:
    loads('{"a": [1, 2.5e2, "x\\n", true, null]}') == {"a": [1, 250.0, "x\n", True, None]}
    loads('"\\u0041"') == "A"
    loads('01')            -> ValueError
    loads('[1,]')          -> ValueError
    loads('{} tail')       -> ValueError
"""


def loads(text: str):
    raise NotImplementedError
