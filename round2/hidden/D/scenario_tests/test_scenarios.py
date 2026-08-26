"""Hidden scenario tests for track D.

Each test boots mockserver.py in-process on an ephemeral port with injected
failure scripts and exercises the candidate's ApiClient against it.
"""

import pytest

from mockserver import serve
from client import ApiClient, ApiError, AuthError


class RecordingSleeper:
    def __init__(self):
        self.calls = []

    def __call__(self, seconds):
        self.calls.append(float(seconds))


def make(script=None, items=None, **kw):
    handle = serve(items=items, script=script if script is not None else [None])
    sleeper = RecordingSleeper()
    client = ApiClient(handle.base_url, sleeper=sleeper, **kw)
    return handle, client, sleeper


def teardown(handle):
    handle.shutdown()


def test_list_all_paginates_completely():
    h, c, _ = make(items=[{"id": i} for i in range(1, 58)], script=[None])
    try:
        got = c.list_all()
        assert [x["id"] for x in got] == list(range(1, 58))
    finally:
        teardown(h)


def test_list_all_survives_500_and_429():
    # first request 500, second 429 (Retry-After 1), then normal pages
    h, c, s = make(script=["500", "429", None])
    try:
        got = c.list_all()
        assert len(got) == 57
        assert any(x == 1.0 for x in s.calls)          # Retry-After honored
    finally:
        teardown(h)


def test_retry_exhaustion_raises_with_attempts():
    h, c, _ = make(script=["500"], max_retries=3)
    try:
        with pytest.raises(ApiError) as ei:
            c.list_all()
        assert ei.value.attempts == 3
    finally:
        teardown(h)


def test_create_order_silent_refresh_once():
    h, c, _ = make(script=[None])                      # token defaults to tok-stale
    try:
        out = c.create_order({"sku": "x1", "qty": 2})
        assert out["order_id"].startswith("ord-")
        assert out["sku"] == "x1"
        assert h.state.refresh_count == 1              # exactly one refresh
        assert c.token == "tok-live"                   # new bearer stored
        # second order needs NO further refresh
        c.create_order({"sku": "x2"})
        assert h.state.refresh_count == 1
    finally:
        teardown(h)


def test_create_order_bad_refresh_raises_autherror():
    h, c, _ = make(script=[None], refresh_token="wrong")
    try:
        with pytest.raises(AuthError):
            c.create_order({"sku": "y"})
    finally:
        teardown(h)


def test_valid_token_needs_no_refresh():
    h, c, _ = make(script=[None])
    try:
        c.token = "tok-live"                           # already valid
        out = c.create_order({"a": 1})
        assert out["order_id"].startswith("ord-")
        assert h.state.refresh_count == 0
    finally:
        teardown(h)
