# REFACTORS.md — orders_app (all directives are REQUIRED)

The characterization tests (`test_behavior_orders.py`) lock in the current
observable behavior. Every directive below must be completed WITHOUT any
change to observable behavior (receipt strings, error messages, stored
record shapes, public function signatures may only change if a directive
explicitly says so).

R1. Create a new module `taxes.py` that defines `TAX_RATE = 0.08` and a
    function `tax(amount) -> float` returning `round(amount * TAX_RATE, 2)`.
    Both `main.py` and `pricing.py` must use it. After the refactor, the
    literal `0.08` must appear ONLY inside `taxes.py`.

R2. Eliminate the module-level mutable global `ORDERS` dict in `store.py`.
    Replace it with an `OrderStore` class (methods: save_order, get_order,
    clear). Expose one shared instance named `order_store` from `store.py`
    so existing callers keep working with minimal changes.

R3. Split the god-function `process_order` in `main.py` into three
    functions in `main.py`: `validate_order(lines)`, `price_order(lines)`
    (returns a dict with keys subtotal/discount/tax/total), and a slim
    orchestrating `process_order` that calls both plus persists and formats.
    All three must live in `main.py`.

R4. Delete the entirely-dead module `legacy_utils.py` (file must no longer
    exist).

R5. In `pricing.py`, extract the tier logic into a public function
    `discount_rate(subtotal) -> float` (returns 0.10 / 0.05 / 0.0), and make
    `apply_discounts` call it. The tier thresholds stay identical.

R6. Add type hints to every PUBLIC function signature in `main.py`,
    `pricing.py`, `store.py`, and the new `taxes.py`
    (parameters + return annotations).
