"""Mock Items & Orders API server (stdlib only).

Boot it programmatically:

    from mockserver import serve
    handle = serve(items=n, script=[None, "500", "429"], stale_tokens={"tok-old"})
    # handle.base_url -> http://127.0.0.1:<port>
    # handle.shutdown() when done

Endpoints
---------
GET /items?cursor=&page_size=
    Returns JSON {"items": [...], "next_cursor": "<str>" | null}.
    Default page_size is 20 (max 100). Cursor is the next index as a string.
    Every request consumes the NEXT entry of `script` (cycling):
        None  -> normal response
        "500" -> HTTP 500
        "429" -> HTTP 429 with header `Retry-After: 1`
    Requests are counted PER SERVER (not per endpoint).

POST /orders        (header Authorization: Bearer <token>)
    Body JSON echoed into {"order_id": "ord-<n>", ...payload} with 201.
    If the bearer token is missing/wrong or in `stale_tokens`:
        401 {"error": "unauthorized"}

POST /auth/refresh  (JSON body {"refresh_token": "<tok>"})
    If it equals the configured refresh token: 200 {"token": "tok-live"}
    Else: 403 {"error": "invalid refresh"}

The server binds 127.0.0.1 on an ephemeral free port and runs in a daemon
thread. It is fully deterministic given (items, script).
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading


class _State:
    def __init__(self, items, script, refresh_token):
        self.items = items
        self.script = list(script) or [None]
        self.pos = 0
        self.refresh_token = refresh_token
        self.valid_token = "tok-live"
        self.stale_tokens = {"tok-stale"}
        self.orders_served = 0
        self.refresh_count = 0
        self.lock = threading.Lock()

    def next_outcome(self):
        with self.lock:
            out = self.script[self.pos % len(self.script)]
            self.pos += 1
            return out


def _handler(state_holder):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, obj, extra_headers=None):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            for k, v in (extra_headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            outcome = state_holder.next_outcome()
            if outcome == "500":
                return self._send(500, {"error": "boom"})
            if outcome == "429":
                return self._send(429, {"error": "slow down"},
                                  {"Retry-After": "1"})
            from urllib.parse import urlparse, parse_qs

            q = parse_qs(urlparse(self.path).query)
            cursor = int(q.get("cursor", ["0"])[0])
            size = min(int(q.get("page_size", ["20"])[0]), 100)
            chunk = state_holder.items[cursor:cursor + size]
            nxt = cursor + len(chunk)
            self._send(200, {
                "items": chunk,
                "next_cursor": str(nxt) if nxt < len(state_holder.items) else None,
            })

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            auth = self.headers.get("Authorization", "")
            path = self.path
            if path.startswith("/auth/refresh"):
                if payload.get("refresh_token") == state_holder.refresh_token:
                    state_holder.refresh_count += 1
                    return self._send(200, {"token": state_holder.valid_token})
                return self._send(403, {"error": "invalid refresh"})
            if path.startswith("/orders"):
                token = auth.replace("Bearer ", "")
                if token != state_holder.valid_token or \
                        token in state_holder.stale_tokens:
                    return self._send(401, {"error": "unauthorized"})
                state_holder.orders_served += 1
                out = {"order_id": f"ord-{state_holder.orders_served}",
                       **payload}
                return self._send(201, out)
            self._send(404, {"error": "not found"})

    return H


class ServerHandle:
    def __init__(self, httpd, state):
        self.httpd = httpd
        self.state = state
        self.base_url = f"http://127.0.0.1:{httpd.server_port}"

    def shutdown(self):
        self.httpd.shutdown()
        self.httpd.server_close()


def serve(items=None, script=None, refresh_token="refresh-xyz") -> ServerHandle:
    items = items if items is not None else [
        {"id": i, "name": f"item-{i}"} for i in range(1, 58)
    ]
    st = _State(items, script if script is not None else [None], refresh_token)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _handler(st))
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return ServerHandle(httpd, st)


if __name__ == "__main__":
    h = serve(script=[None])
    print("serving at", h.base_url)
