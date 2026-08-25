from registry import Registry


class App:
    def __init__(self):
        self.registry = Registry()
        self._middlewares = []

    def use(self, middleware) -> None:
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
            if i >= len(self._middlewares):
                handler, params = resolved
                return handler(params, ctx)
            mw = self._middlewares[i]
            return mw(ctx, lambda: run(i + 1))

        return run(0)
