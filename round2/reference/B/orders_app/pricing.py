"""Pricing helpers."""

from typing import List, Tuple

import taxes


def discount_rate(subtotal: float) -> float:
    if subtotal >= 500:
        return 0.10
    if subtotal >= 100:
        return 0.05
    return 0.0


def apply_discounts(lines: List[Tuple[float, int]]) -> float:
    subtotal = _subtotal(lines)
    return subtotal * (1 - discount_rate(subtotal))


def calc_tax(amount: float) -> float:
    return taxes.tax(amount)


def _subtotal(lines: List[Tuple[float, int]]) -> float:
    total = 0.0
    for price, qty in lines:
        total += price * qty
    return total
