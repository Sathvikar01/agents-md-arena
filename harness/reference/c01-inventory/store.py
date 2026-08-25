from collections import defaultdict


class Inventory:
    def __init__(self):
        self._on_hand: defaultdict = defaultdict(int)
        self._reserved: defaultdict = defaultdict(int)

    def add(self, sku: str, qty: int) -> None:
        if qty < 0:
            raise ValueError("qty must be >= 0")
        self._on_hand[sku] += qty

    def remove(self, sku: str, qty: int) -> bool:
        if qty < 0:
            raise ValueError("qty must be >= 0")
        if self.available(sku) < qty:
            return False
        self._on_hand[sku] -= qty
        return True

    def available(self, sku: str) -> int:
        return self._on_hand[sku] - self._reserved[sku]

    def reserve(self, sku: str, qty: int) -> bool:
        if qty <= 0:
            return False
        if self.available(sku) < qty:
            return False
        self._reserved[sku] += qty
        return True

    def release(self, sku: str, qty: int) -> bool:
        if self._reserved.get(sku, 0) < qty:
            return False
        self._reserved[sku] -= qty
        return True
