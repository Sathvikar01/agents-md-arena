"""Pricing helpers (legacy)."""


def apply_discounts(lines):
    """lines: list of (unit_price:int cents-free float, qty:int). Returns discounted subtotal."""
    subtotal = 0.0
    for price, qty in lines:
        if qty < 1:
            raise ValueError("invalid quantity")
        subtotal += price * qty
    # tiered discounts
    if subtotal >= 500:
        return subtotal * 0.90
    if subtotal >= 100:
        return subtotal * 0.95
    return subtotal


def calc_tax(amount):
    return round(amount * 0.08, 2)


# NOTE(maintainer): tax logic copied here AND inlined in main.process_order --
# keep them in sync!
