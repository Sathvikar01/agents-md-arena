"""Route registry: first matching pattern in registration order wins."""


class Registry:
    def __init__(self):
        self._routes = []  # (method, pattern, handler)

    def add(self, method: str, pattern: str, handler) -> None:
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._routes.append((method.upper(), pattern, handler))

    def resolve(self, method: str, path: str):
        """Return (handler, params) for the first match, else None."""
        from matcher import match

        for m, pattern, handler in self._routes:
            if m != method.upper():
                continue
            params = match(pattern, path)
            if params is not None:
                return (handler, params)
        return None
