"""HTTP client for the Items & Orders API. Implement per API_SPEC.md.

Grading scenario tests boot mockserver.py with injected failures and assert:
  - list_all() returns all items in order despite interleaved 500/429,
    sleeping via the injected sleeper (Retry-After honored),
  - ApiError raised (with .attempts == max_retries) when retries exhaust,
  - create_order() silently refreshes a stale token exactly once then
    succeeds; AuthError on failed refresh / repeated 401.
"""

import json
import time
from urllib import request as _rq
from urllib.error import HTTPError


class ApiError(Exception):
    def __init__(self, msg: str, attempts: int = 0):
        super().__init__(msg)
        self.attempts = attempts


class AuthError(ApiError):
    pass


class ApiClient:
    def __init__(self, base_url: str, token: str = "tok-stale",
                 refresh_token: str = "refresh-xyz", max_retries: int = 5,
                 backoff_base: float = 0.05, sleeper=time.sleep):
        raise NotImplementedError

    def list_all(self) -> list:
        """Fetch every item across all pages, in order."""
        raise NotImplementedError

    def create_order(self, payload: dict) -> dict:
        """Create an order; silent single token refresh on 401."""
        raise NotImplementedError

    def refresh(self) -> None:
        """Exchange refresh_token for a new bearer token."""
        raise NotImplementedError
