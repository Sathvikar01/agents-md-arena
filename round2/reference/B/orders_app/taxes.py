TAX_RATE = 0.08


def tax(amount: float) -> float:
    return round(amount * TAX_RATE, 2)
