from models import OrderLine


def _discount_rate(qty: int) -> float:
    if qty >= 50:
        return 0.10
    if qty >= 10:
        return 0.05
    return 0.0


def line_total(line: OrderLine) -> float:
    gross = line.product.unit_price * line.quantity
    return round(gross * (1 - _discount_rate(line.quantity)), 2)


def order_total(lines: list[OrderLine]) -> float:
    return round(sum(line_total(l) for l in lines), 2)
