"""Order persistence."""

from typing import Dict, Optional


class OrderStore:
    def __init__(self) -> None:
        self._orders: Dict[str, dict] = {}

    def save_order(self, order_id: str, record: dict) -> str:
        self._orders[order_id] = record
        return order_id

    def get_order(self, order_id: str) -> Optional[dict]:
        return self._orders.get(order_id)

    def clear(self) -> None:
        self._orders.clear()


order_store = OrderStore()


def save_order(order_id: str, record: dict) -> str:
    return order_store.save_order(order_id, record)


def get_order(order_id: str) -> Optional[dict]:
    return order_store.get_order(order_id)


def clear() -> None:
    return order_store.clear()
