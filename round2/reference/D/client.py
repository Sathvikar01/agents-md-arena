"""Reference implementation for track D."""

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
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.refresh_token = refresh_token
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.sleeper = sleeper

    # ---------------- internals ----------------

    def _request(self, method: str, path: str, body=None,
                 extra_headers=None) -> tuple:
        """One HTTP attempt -> (status, parsed_body|None, headers)."""
        url = self.base_url + path
        data = json.dumps(body).encode() if body is not None else None
        req = _rq.Request(url, data=data, method=method)
        for k, v in (extra_headers or {}).items():
            req.add_header(k, v)
        try:
            with _rq.urlopen(req, timeout=10) as resp:
                raw = resp.read()
                return resp.status, (json.loads(raw) if raw else None), dict(resp.headers)
        except HTTPError as e:
            raw = e.read()
            try:
                parsed = json.loads(raw) if raw else None
            except Exception:
                parsed = None
            return e.code, parsed, dict(e.headers)

    @staticmethod
    def _is_transient(status: int) -> bool:
        return status == 429 or 500 <= status < 600

    def _sleep_before_retry(self, status: int, attempt: int,
                            headers: dict) -> None:
        ra = headers.get("Retry-After")
        if ra is not None:
            try:
                self.sleeper(float(ra))
                return
            except ValueError:
                pass
        self.sleeper(self.backoff_base * (2 ** (attempt - 1)))

    def _get_json_retry(self, path: str) -> dict:
        attempts = 0
        while True:
            status, body, headers = self._request("GET", path)
            attempts += 1
            if status == 200 and isinstance(body, dict):
                return body
            if not self._is_transient(status) or attempts >= self.max_retries:
                raise ApiError(
                    f"GET {path} failed after {attempts} attempts "
                    f"(last status {status})", attempts=attempts)
            self._sleep_before_retry(status, attempts, headers)

    # ---------------- public API ----------------

    def refresh(self) -> None:
        status, body, _ = self._request(
            "POST", "/auth/refresh",
            body={"refresh_token": self.refresh_token})
        if status != 200 or not isinstance(body, dict) or "token" not in body:
            raise AuthError("token refresh failed", attempts=1)
        self.token = body["token"]

    def list_all(self) -> list:
        items = []
        cursor = None
        while True:
            path = "/items?page_size=20"
            if cursor is not None:
                path += f"&cursor={cursor}"
            page = self._get_json_retry(path)
            items.extend(page["items"])
            nxt = page.get("next_cursor")
            if nxt is None:
                return items
            cursor = nxt

    def create_order(self, payload: dict) -> dict:
        refreshed = False
        attempts = 0
        while True:
            attempts += 1
            status, body, headers = self._request(
                "POST", "/orders", body=payload,
                extra_headers={"Authorization": f"Bearer {self.token}"})
            if status == 201:
                return body
            if status == 401:
                if refreshed:
                    raise AuthError("still unauthorized after refresh",
                                    attempts=attempts)
                refreshed = True
                self.refresh()
                continue
            if not self._is_transient(status):
                raise ApiError(f"POST /orders rejected: {status}",
                               attempts=attempts)
            if attempts >= self.max_retries:
                raise ApiError(f"POST /orders failed after {attempts} attempts "
                               f"(last status {status})", attempts=attempts)
            self._sleep_before_retry(status, attempts, headers)
