# API Spec — Items & Orders (served by `mockserver.py`)

Read `mockserver.py` source too — it is the ground truth for exact behaviors.
Summary of what YOUR client (`client.py`) must handle:

## GET /items
- Cursor pagination: response `{"items": [...], "next_cursor": "20"|null}`.
  Pass `cursor=<str>` and optionally `page_size=` (server default 20).
  **list_all() must fetch EVERY item exactly once, in server order**, across
  all pages, regardless of page size.

## Transient failures
- The server may answer `500` or `429` (with header `Retry-After: <seconds>`).
- On 500 or 429 the client must RETRY the same request, sleeping between
  attempts: sleep `Retry-After` seconds when present, otherwise
  `backoff_base * 2**attempt` seconds. Sleeps go through the injectable
  `sleeper` constructor argument (so tests can observe without waiting).
- Give up after `max_retries` consecutive failed attempts of a single
  logical step, raising `ApiError("...", attempts=<n>)`.
- Successful responses reset the consecutive-failure counter.

## POST /orders
- Header `Authorization: Bearer <token>`, JSON body = payload dict.
- 201 → returns parsed body.
- 401 means the token is stale: call `POST /auth/refresh`
  with `{"refresh_token": <refresh_token>}`; store the returned `token` as
  the new bearer token AND retry the order creation EXACTLY ONCE more.
  This silent-refresh may happen at most once per create_order call.
- If refresh returns 403, or the retried request is 401 again, raise
  `AuthError`.

## Errors hierarchy
```python
class ApiError(Exception): ...      # has .attempts attribute on retry exhaustion
class AuthError(ApiError): ...
```

## Constructor contract
```python
ApiClient(base_url, token="tok-stale", refresh_token="refresh-xyz",
          max_retries=5, backoff_base=0.05, sleeper=time.sleep)
```
