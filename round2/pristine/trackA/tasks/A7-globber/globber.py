"""Glob-style path matcher.

Contract — implement match(pattern, path, sep='/') exactly:

match(pattern: str, path: str, sep: str = '/') -> bool

Rules:
    - Both pattern and path are split on `sep` into SEGMENTS.
    - '?' inside a pattern segment matches EXACTLY ONE character within a
      single path segment (never matches the separator).
    - '*' inside a pattern segment matches ZERO OR MORE characters within a
      single path segment (never crosses a separator).
    - '**' as an ENTIRE pattern segment matches ZERO or more whole path
      segments (including empty ones). It must be the full segment to have
      this power: 'a*b' contains no '**' magic even if written 'a**b'.
    - Any other segment characters match literally.
    - The whole path must be consumed for a match (full match).
    - Empty pattern matches only empty path. Pattern '' vs path 'a' -> False,
      pattern 'a/' vs path 'a' -> False (trailing sep creates an empty final
      segment which must correspondingly exist in the other string).

Examples:
    match('*.txt', 'notes.txt')            -> True
    match('*.txt', 'dir/notes.txt')        -> False   (* cannot cross '/')
    match('**', 'a/b/c')                   -> True
    match('a/**/b', 'a/b')                 -> True     (** may match zero segments)
    match('a/**/b', 'a/x/y/b')             -> True
    match('/user/:id'.replace(':id','*'), '/user/42') -> True
    match('a?c', 'abc')                    -> True
    match('a?c', 'ac')                     -> False
"""


def match(pattern: str, path: str, sep: str = "/") -> bool:
    raise NotImplementedError
