"""Deterministically build the analytics database.

Usage: python db_generator.py [output_path]

The output is byte-for-byte reproducible (seeded RNG, fixed insertion order).
Schema:

    customers(id INTEGER PK, name TEXT, country TEXT, joined_at TEXT)
    products(id INTEGER PK, name TEXT, category TEXT, price REAL)
    orders(id INTEGER PK, customer_id INT, created_at TEXT, status TEXT)
    order_items(order_id INT, product_id INT, qty INT, unit_price REAL)

created_at format: 'YYYY-MM-DD HH:MM:SS'. status is one of
'paid', 'pending', 'cancelled'. Some products are never ordered.
"""

import os
import random
import sqlite3
import sys
from datetime import datetime, timedelta

FIRST = ["Anna", "Ben", "Clara", "David", "Elif", "Finn", "Greta", "Hans",
         "Ines", "Jonas", "Kara", "Liam", "Mara", "Noah", "Olga", "Paul",
         "Quinn", "Rita", "Sven", "Tara", "Ulf", "Vera", "Will", "Xenia",
         "Yusuf", "Zoe", "Amelie", "Anton", "Astrid", "Anke"]
COUNTRIES = ["DE", "FR", "US", "GB", "NL"]
CATEGORIES = {
    "peripherals": ["Mech Keyboard", "Wireless Mouse", "USB Hub", "Webcam HD",
                    "Desk Mat"],
    "audio": ["Studio Headphones", "BT Speaker", "USB Mic", "Earbuds Pro"],
    "storage": ["SSD 1TB", "SSD 2TB", "HDD 4TB", "MicroSD 256GB"],
    "displays": ["24in IPS", "27in 4K", "34in Ultrawide"],
    "network": ["Wifi 6 Router", "8-port Switch", "Mesh Node"],
}
STATUSES = ["paid", "paid", "paid", "paid", "pending", "cancelled"]


def build(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
    rng = random.Random(20260826)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, country TEXT,
                           joined_at TEXT);
    CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT, category TEXT,
                          price REAL);
    CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER,
                        created_at TEXT, status TEXT);
    CREATE TABLE order_items(order_id INTEGER, product_id INTEGER,
                             qty INTEGER, unit_price REAL);
    """)

    names = []
    for i, first in enumerate(FIRST):
        names.append(f"{first} {chr(65 + i % 26)}erhoff")
        if len(names) >= len(FIRST):
            break
    for i, name in enumerate(names, start=1):
        joined = datetime(2024, 1, 1) + timedelta(days=rng.randrange(0, 700))
        cur.execute("INSERT INTO customers VALUES(?,?,?,?)",
                    (i, name, rng.choice(COUNTRIES),
                     joined.strftime("%Y-%m-%d")))

    pid = 1
    for cat, prods in sorted(CATEGORIES.items()):
        for pname in prods:
            price = round(rng.uniform(9.0, 480.0), 2)
            cur.execute("INSERT INTO products VALUES(?,?,?,?)",
                        (pid, f"{pname}", cat, price))
            pid += 1
    n_products = pid - 1

    base = datetime(2026, 1, 1)
    oid = 1
    for _ in range(140):
        cust = rng.randrange(1, len(names) + 1)
        ts = base + timedelta(minutes=rng.randrange(0, 181 * 24 * 60))
        status = rng.choice(STATUSES)
        cur.execute("INSERT INTO orders VALUES(?,?,?,?)",
                    (oid, cust, ts.strftime("%Y-%m-%d %H:%M:%S"), status))
        for _ in range(rng.randrange(1, 5)):
            p = rng.randrange(1, n_products + 1)
            cur.execute("SELECT price FROM products WHERE id=?", (p,))
            unit = cur.fetchone()[0]
            cur.execute("INSERT INTO order_items VALUES(?,?,?,?)",
                        (oid, p, rng.randrange(1, 4), unit))
        oid += 1

    # guarantee some never-ordered products: kill every item referencing the
    # last two products by moving those lines to other products
    dead = [n_products - 1, n_products]
    cur.execute("DELETE FROM order_items WHERE product_id=?", (dead[0],))
    cur.execute("DELETE FROM order_items WHERE product_id=?", (dead[1],))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "ecommerce.db"
    build(out)
    print(f"built {out}")
