"""Roman numerals, strict canonical forms only.

Contract:

to_int(s: str) -> int
    Parse a roman numeral in UPPERCASE canonical subtractive notation.
    Raise ValueError for ANY of:
      - empty string / non-string input
      - lowercase letters (e.g. 'xiv') or any character outside IVXLCDM
      - non-canonical forms:
          * more than 3 consecutive I, X, C (e.g. 'IIII')
          * any repetition of V, L, D (e.g. 'VV')
          * invalid subtractive pairs — ONLY these six are legal:
            IV IX XL XC CD CM
            so 'IC', 'IL', 'XM', 'VX', 'LC', 'DM' etc. raise ValueError
          * a smaller value before a larger one unless forming a legal pair

from_int(n: int) -> str
    Canonical subtractive form; 1 <= n <= 3999 else ValueError.
    Non-int input raises ValueError.

Round-trip guarantee: from_int(to_int(s)) == s for every canonical s, and
to_int(from_int(n)) == n for all valid n.

Examples:
    to_int('MCMXCIV') == 1994 ; to_int('III') == 3 ; to_int('XL') == 40
    from_int(2026) == 'MMXXVI' ; from_int(3999) == 'MMMCMXCIX'
    to_int('ii'), to_int('IIII'), to_int('IC'), from_int(0), from_int(4000)
    all raise ValueError.
"""

def to_int(s: str) -> int:
    raise NotImplementedError


def from_int(n: int) -> str:
    raise NotImplementedError
