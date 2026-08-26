"""Order entry point (legacy god-function)."""

import store
import pricing


def process_order(order_id, lines, customer):
    if not lines:
        raise ValueError("empty order")
    # validate + subtotal
    subtotal = 0.0
    for price, qty in lines:
        if qty < 1:
            raise ValueError("invalid quantity")
        subtotal += price * qty

    # discounts (duplicate of pricing.apply_discounts logic!)
    if subtotal >= 500:
        disc_sub = subtotal * 0.90
        d_amt = subtotal * 0.10
    elif subtotal >= 100:
        disc_sub = subtotal * 0.95
        d_amt = subtotal * 0.05
    else:
        disc_sub = subtotal
        d_amt = 0.0

    t = round(disc_sub * 0.08, 2)          # duplicate tax logic!
    total = round(disc_sub + t, 2)

    receipt = (
        f"ORDER {order_id} FOR {customer}\n"
        f"SUBTOTAL: {subtotal:.2f}\n"
        f"DISCOUNT: -{d_amt:.2f}\n"
        f"TAX: {t:.2f}\n"
        f"TOTAL: {total:.2f}"
    )
    store.save_order(order_id, {
        "customer": customer,
        "subtotal": subtotal,
        "discount": round(d_amt, 2),
        "tax": t,
        "total": total,
    })
    return receipt
