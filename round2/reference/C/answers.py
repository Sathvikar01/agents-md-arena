"""Reference answers for track C (defines the expected results)."""


def q01(conn):
    return conn.execute(
        "SELECT id, name FROM customers WHERE country = 'DE'").fetchall()


def q02(conn):
    return conn.execute("""
        SELECT oi.product_id, ROUND(SUM(oi.qty * oi.unit_price), 2) AS rev
        FROM order_items oi
        JOIN orders o ON o.id = oi.order_id
        WHERE o.status = 'paid'
        GROUP BY oi.product_id
        ORDER BY rev DESC, oi.product_id ASC
        LIMIT 3
    """).fetchall()


def q03(conn):
    return conn.execute(
        "SELECT status, COUNT(*) FROM orders GROUP BY status").fetchall()


def q04(conn):
    return conn.execute("""
        SELECT strftime('%Y-%m', created_at),
               ROUND(SUM(q), 2)
        FROM (
            SELECT o.created_at, SUM(oi.qty * oi.unit_price) AS q
            FROM orders o JOIN order_items oi ON oi.order_id = o.id
            WHERE o.status = 'paid'
            GROUP BY o.id, o.created_at
        )
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY 1 ASC
    """).fetchall()


def q05(conn):
    return conn.execute("""
        SELECT c.id, c.name FROM customers c
        WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
        ORDER BY c.name ASC, c.id ASC
    """).fetchall()


def q06(conn):
    return conn.execute("""
        SELECT ROUND(AVG(v), 2) FROM (
            SELECT SUM(oi.qty * oi.unit_price) AS v
            FROM orders o JOIN order_items oi ON oi.order_id = o.id
            WHERE o.status = 'paid'
            GROUP BY o.id
        )
    """).fetchall()


def q07(conn):
    return conn.execute("""
        SELECT p.id, p.name FROM products p
        WHERE NOT EXISTS (
            SELECT 1 FROM order_items oi WHERE oi.product_id = p.id)
        ORDER BY p.id ASC
    """).fetchall()


def q08(conn):
    return conn.execute("""
        SELECT c.id, COUNT(o.id) FROM customers c
        LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'paid'
        GROUP BY c.id ORDER BY c.id ASC
    """).fetchall()


def q09(conn):
    return conn.execute("""
        SELECT oi.order_id, oi.product_id, oi.qty * oi.unit_price AS line
        FROM order_items oi
        JOIN orders o ON o.id = oi.order_id
        WHERE o.status = 'paid'
        ORDER BY line DESC, oi.order_id ASC
        LIMIT 1
    """).fetchall()


def q10(conn):
    return conn.execute("""
        SELECT ROUND(100.0 * SUM(CASE WHEN status != 'paid' THEN 1 ELSE 0 END)
                     / COUNT(*), 2)
        FROM orders
    """).fetchall()


def q11(conn):
    return conn.execute(
        "SELECT DISTINCT country FROM customers ORDER BY country ASC"
    ).fetchall()


def q12(conn):
    return conn.execute("""
        SELECT p.category, ROUND(SUM(oi.qty * oi.unit_price), 2) AS rev
        FROM order_items oi
        JOIN orders o ON o.id = oi.order_id
        JOIN products p ON p.id = oi.product_id
        WHERE o.status = 'paid'
          AND strftime('%Y-%m', o.created_at) = '2026-06'
        GROUP BY p.category
        ORDER BY rev DESC, p.category ASC
    """).fetchall()


def q13(conn):
    return conn.execute("""
        SELECT name FROM customers WHERE name LIKE 'A%' ORDER BY name ASC
    """).fetchall()


def q14(conn):
    return conn.execute("""
        SELECT category, MIN(price), MAX(price)
        FROM products GROUP BY category ORDER BY category ASC
    """).fetchall()


def q15(conn):
    return conn.execute("""
        SELECT order_id, COUNT(DISTINCT product_id) AS d
        FROM order_items GROUP BY order_id HAVING d >= 2
        ORDER BY d DESC, order_id ASC
    """).fetchall()
