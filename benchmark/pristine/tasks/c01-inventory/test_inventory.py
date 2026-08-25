import pytest
from models import Product, OrderLine
from pricing import line_total, order_total, _discount_rate
from store import Inventory

PEN = Product("pen-1", "Gel Pen", 2.0)
BOOK = Product("book-9", "Notebook", 10.0)


# ---------- models ----------

def test_product_fields():
    assert PEN.sku == "pen-1" and PEN.name == "Gel Pen" and PEN.unit_price == 2.0


def test_order_line_holds_product_and_qty():
    ol = OrderLine(PEN, 3)
    assert ol.product is PEN and ol.quantity == 3


def test_product_is_frozen():
    with pytest.raises(Exception):
        PEN.sku = "x"


# ---------- pricing ----------

def test_no_discount_below_10():
    assert _discount_rate(9) == 0.0
    assert line_total(OrderLine(PEN, 9)) == 18.0


def test_small_tier_starts_at_10():
    assert _discount_rate(10) == 0.05
    assert line_total(OrderLine(BOOK, 10)) == 95.0  # 100 - 5%


def test_large_tier_starts_exactly_at_50():
    assert _discount_rate(50) == 0.10
    # boundary: qty 49 must NOT get the large discount
    assert _discount_rate(49) == 0.05
    assert line_total(OrderLine(BOOK, 49)) == round(490 * 0.95, 2)
    assert line_total(OrderLine(BOOK, 50)) == round(500 * 0.90, 2)


def test_order_total_sums_lines_independently():
    total = order_total([OrderLine(PEN, 12), OrderLine(BOOK, 5)])
    assert total == round(24 * 0.95 + 50.0, 2)


# ---------- inventory ----------

def test_add_and_available():
    inv = Inventory()
    inv.add("sku", 5)
    assert inv.available("sku") == 5


def test_unknown_sku_available_zero():
    assert Inventory().available("ghost") == 0


def test_remove_fails_when_insufficient():
    inv = Inventory()
    inv.add("sku", 2)
    assert inv.remove("sku", 3) is False
    assert inv.remove("sku", 2) is True
    assert inv.available("sku") == 0


def test_reserve_respects_reservations():
    inv = Inventory()
    inv.add("sku", 10)
    assert inv.reserve("sku", 6) is True
    # only 4 available now: another reserve of 6 must fail
    assert inv.reserve("sku", 6) is False
    assert inv.reserve("sku", 4) is True


def test_release_returns_to_pool():
    inv = Inventory()
    inv.add("sku", 10)
    inv.reserve("sku", 8)
    assert inv.available("sku") == 2
    assert inv.release("sku", 9) is False  # more than reserved
    assert inv.release("sku", 8) is True
    assert inv.available("sku") == 10


def test_remove_negative_qty_raises():
    inv = Inventory()
    with pytest.raises(ValueError):
        inv.add("s", -1)
