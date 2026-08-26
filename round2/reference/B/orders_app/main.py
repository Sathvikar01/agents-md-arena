"""Order entry point."""

from typing import List, Tuple

import pricing
import taxes
import store


def validate_order(lines: List[Tuple[float, int]]) -> float:
    if not lines:
        raise ValueError("empty order")
    subtotal = 0.0
    for price, qty in lines:
        if qty < 1:
            raise ValueError("invalid quantity")
        subtotal += price * qty
    return subtotal


def price_order(subtotal: float) -> dict:
    rate = pricing.discount_rate(subtotal)
    disc_sub = subtotal * (1 - rate)
    d_amt = subtotal * rate
    t = taxes.tax(disc_sub)
    total = round(disc_sub + t, 2)
    return {"subtotal": subtotal, "discount": round(d_amt, 2),
            "tax": t, "total": total}


def process_order(order_id: str, lines: List[Tuple[float, int]], customer: str) -> str:
    priced = price_order(validate_order(lines))
    receipt = (
        f"ORDER {order_id} FOR {customer}\n"
        f"SUBTOTAL: {priced['subtotal']:.2f}\n"
        f"DISCOUNT: -{priced['discount']:.2f}\n"
        f"TAX: {priced['tax']:.2f}\n"
        f"TOTAL: {priced['total']:.2f}"
    )
    store.order_store.save_order(order_id, {
        "customer": customer,
        **priced,
    })
    return receipt
