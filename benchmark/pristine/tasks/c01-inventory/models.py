from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    unit_price: float


@dataclass(frozen=True)
class OrderLine:
    product: Product
    quantity: int
