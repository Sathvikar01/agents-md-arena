WHITESPACE = " \t\n\r"


class _Parser:
    def __init__(self, text: str):
        self.s = text
        self.i = 0

    def error(self, msg="invalid JSON"):
        raise ValueError(f"{msg} at position {self.i}")

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ""

    def skip_ws(self):
        while self.i < len(self.s) and self.s[self.i] in WHITESPACE:
            self.i += 1

    def parse(self):
        self.skip_ws()
        val = self.value()
        self.skip_ws()
        if self.i != len(self.s):
            self.error("trailing characters")
        return val

    def value(self):
        c = self.peek()
        if c == "{":
            return self.object()
        if c == "[":
            return self.array()
        if c == '"':
            return self.string()
        if c == "-" or c.isdigit():
            return self.number()
        for lit, out in (("true", True), ("false", False), ("null", None)):
            if self.s.startswith(lit, self.i):
                self.i += len(lit)
                return out
        self.error()

    def object(self):
        self.i += 1
        obj = {}
        self.skip_ws()
        if self.peek() == "}":
            self.i += 1
            return obj
        while True:
            self.skip_ws()
            if self.peek() != '"':
                self.error("expected string key")
            key = self.string()
            self.skip_ws()
            if self.peek() != ":":
                self.error("expected ':'")
            self.i += 1
            self.skip_ws()
            obj[key] = self.value()
            self.skip_ws()
            c = self.peek()
            if c == ",":
                self.i += 1
                continue
            if c == "}":
                self.i += 1
                return obj
            self.error("expected ',' or '}'")

    def array(self):
        self.i += 1
        arr = []
        self.skip_ws()
        if self.peek() == "]":
            self.i += 1
            return arr
        while True:
            self.skip_ws()
            arr.append(self.value())
            self.skip_ws()
            c = self.peek()
            if c == ",":
                self.i += 1
                continue
            if c == "]":
                self.i += 1
                return arr
            self.error("expected ',' or ']'")

    def string(self):
        self.i += 1
        out = []
        while True:
            if self.i >= len(self.s):
                self.error("unterminated string")
            c = self.s[self.i]
            if c == '"':
                self.i += 1
                return "".join(out)
            if ord(c) < 0x20:
                self.error("raw control character")
            if c == "\\":
                self.i += 1
                esc = self.peek()
                simple = {'"': '"', "\\": "\\", "/": "/",
                          "b": "\b", "f": "\f", "n": "\n",
                          "r": "\r", "t": "\t"}
                if esc in simple:
                    out.append(simple[esc])
                    self.i += 1
                elif esc == "u":
                    hexpart = self.s[self.i + 1:self.i + 5]
                    if len(hexpart) != 4 or any(
                            ch not in "0123456789abcdefABCDEF" for ch in hexpart):
                        self.error("bad \\u escape")
                    out.append(chr(int(hexpart, 16)))
                    self.i += 5
                else:
                    self.error("bad escape")
            else:
                out.append(c)
                self.i += 1

    def number(self):
        start = self.i
        if self.peek() == "-":
            self.i += 1
        if self.peek() == "0":
            self.i += 1
        elif self.peek().isdigit():
            while self.peek().isdigit():
                self.i += 1
        else:
            self.error("bad number")
        is_float = False
        if self.peek() == ".":
            is_float = True
            self.i += 1
            if not self.peek().isdigit():
                self.error("bad number")
            while self.peek().isdigit():
                self.i += 1
        if self.peek() in ("e", "E"):
            is_float = True
            self.i += 1
            if self.peek() in ("+", "-"):
                self.i += 1
            if not self.peek().isdigit():
                self.error("bad number")
            while self.peek().isdigit():
                self.i += 1
        lit = self.s[start:self.i]
        return float(lit) if is_float else int(lit)


def loads(text: str):
    if not isinstance(text, str):
        raise ValueError("input must be str")
    return _Parser(text).parse()
