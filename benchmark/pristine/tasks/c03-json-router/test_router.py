import pytest
from matcher import match
from app import App


# ---------- matcher ----------

def test_static_pattern():
    assert match("/health", "/health") == {}


def test_param_captures_single_segment():
    assert match("/user/:id", "/user/42") == {"id": "42"}


def test_param_does_not_span_slashes():
    assert match("/user/:id", "/user/42/posts") is None


def test_extra_segments_fail():
    assert match("/user/:id", "/user/1/2") is None


def test_multiple_params():
    got = match("/org/:org/repo/:repo", "/org/acme/repo/web")
    assert got == {"org": "acme", "repo": "web"}


def test_literal_mismatch():
    assert match("/user/:id", "/users/42") is None


def test_trailing_slash_is_a_different_path():
    assert match("/health", "/health/") is None


def test_empty_param_segment_fails():
    assert match("/user/:id", "/user/") is None


# ---------- app / registry / integration ----------

@pytest.fixture()
def app():
    a = App()

    @a.route("GET", "/hello")
    def hello(params, ctx):
        return {"msg": "hi", "seen": ctx.get("seen", [])}

    @a.route("GET", "/user/:id")
    def user(params, ctx):
        return {"user": params["id"]}

    return a


def test_unknown_route_returns_none(app):
    assert app.handle("GET", "/nope") is None


def test_wrong_method_no_match(app):
    assert app.handle("POST", "/hello") is None


def test_route_with_params(app):
    assert app.handle("GET", "/user/7") == {"user": "7"}


def test_first_registered_route_wins():
    a = App()
    a.registry.add("GET", "/x/:a", lambda p, c: "first")
    a.registry.add("GET", "/x/static", lambda p, c: "second")
    assert a.handle("GET", "/x/static") == "first"


def test_middleware_registration_order():
    a = App()
    order = []

    def first(ctx, nxt):
        order.append("first")
        return nxt()

    def second(ctx, nxt):
        order.append("second")
        return nxt()

    a.use(first)
    a.use(second)
    a.route("GET", "/p")(lambda p, c: "ok")

    assert a.handle("GET", "/p") == "ok"
    assert order == ["first", "second"]


def test_middleware_can_shortcircuit():
    a = App()

    def guard(ctx, nxt):
        return "blocked"

    a.use(guard)
    a.route("GET", "/s")(lambda p, c: "never")

    assert a.handle("GET", "/s") == "blocked"


def test_ctx_flows_to_handler():
    a = App()

    def inject(ctx, nxt):
        ctx["token"] = "t1"
        return nxt()

    a.use(inject)
    a.route("GET", "/me")(lambda p, c: c.get("token"))

    assert a.handle("GET", "/me") == "t1"
