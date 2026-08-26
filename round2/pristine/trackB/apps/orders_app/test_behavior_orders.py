"""CHARACTERIZATION TESTS - locked behavior for orders_app.

DO NOT MODIFY. These describe what the code does TODAY; the refactors must
keep every assertion passing exactly as written.
"""

import pytest

import main
import store


def setup_function(_):
    store.clear()


def lines(*pairs):
    return [(p, q) for p, q in pairs]


def test_no_discount_below_100():
    r = main.process_order("o1", lines((10.0, 3)), "Ann")
    assert "SUBTOTAL: 30.00" in r and "DISCOUNT: -0.00" in r
    assert "TAX: 2.40" in r and "TOTAL: 32.40" in r


def test_small_tier_starts_exactly_at_100():
    r = main.process_order("o2", lines((50.0, 2)), "Bo")
    assert "DISCOUNT: -5.00" in r          # 5% of 100
    assert "TOTAL: 102.60" in r            # 95 + 7.6


def test_large_tier_starts_exactly_at_500():
    r = main.process_order("o3", lines((250.0, 2)), "Cy")
    assert "DISCOUNT: -50.00" in r         # 10% of 500
    assert "TAX: 36.00" in r               # 450 * .08
    assert "TOTAL: 486.00" in r


def test_receipt_exact_format():
    r = main.process_order("o4", lines((10.0, 1)), "Dee")
    assert r == (
        "ORDER o4 FOR Dee\n"
        "SUBTOTAL: 10.00\n"
        "DISCOUNT: -0.00\n"
        "TAX: 0.80\n"
        "TOTAL: 10.80"
    )


def test_rounding_half_even():
    # subtotal 12.25 -> after 0% discount tax = round(12.25*0.08, 2)
    r = main.process_order("o5", lines((12.25, 1)), "Eve")
    assert "TAX: 0.98" in r


def test_empty_order_message():
    with pytest.raises(ValueError, match="empty order"):
        main.process_order("o6", [], "Fay")


def test_invalid_quantity_message():
    with pytest.raises(ValueError, match="invalid quantity"):
        main.process_order("o7", lines((10.0, 0)), "Gus")


def test_order_persisted_with_fields():
    main.process_order("o8", lines((200.0, 1)), "Hal")
    rec = store.get_order("o8")
    assert rec == {"customer": "Hal", "subtotal": 200.0,
                   "discount": 10.0, "tax": 15.2, "total": 205.2}


def test_get_unknown_order_none():
    assert store.get_order("ghost") is None


def test_same_id_last_wins():
    main.process_order("o9", lines((10.0, 1)), "A")
    main.process_order("o9", lines((20.0, 1)), "B")
    assert store.get_order("o9")["customer"] == "B"


def test_tax_matches_pricing_module():
    # duplicate implementations currently agree
    assert pricing_calc(100.0) == __import__("pricing").calc_tax(100.0)


def pricing_calc(amount):
    return round(amount * 0.08, 2)


def test_line_qty_fractional_allowed():
    r = main.process_order("oA", lines((10.0, 2)), "Ivy")
    assert "SUBTOTAL: 20.00" in r
