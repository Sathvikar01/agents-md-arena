"""Order persistence. NOTE: intentionally legacy-style."""

ORDERS = {}


def save_order(order_id, record):
    ORDERS[order_id] = record
    return order_id


def get_order(order_id):
    return ORDERS.get(order_id)


def clear():
    ORDERS.clear()
