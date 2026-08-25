"""App with middleware chain.

Middleware run in REGISTRATION order for the request phase; each receives
(ctx, next_handler) and may short-circuit by not calling next_handler.
"""

from registry import Registry


class App:
    def __init__(self):
        self.registry = Registry()
        self._middlewares = []

    def use(self, middleware) -> None:
        """middleware(ctx, next) -> response"""
        if not callable(middleware):
            raise TypeError("middleware must be callable")
        self._middlewares.append(middleware)

    def route(self, method: str, pattern: str):
        def deco(fn):
            self.registry.add(method, pattern, fn)
            return fn

        return deco

    def handle(self, method: str, path: str, ctx: dict | None = None) -> object:
        ctx = ctx if ctx is not None else {}
        resolved = self.registry.resolve(method, path)
        if resolved is None:
            return None

        def run(i):
            if i < 0:
                handler, params = resolved
                return handler(params, ctx)
            mw = self._middlewares[i]
            return mw(ctx, lambda: run(i - 1))

        return run(len(self._middlewares) - 1)
