import sqlite3
from pathlib import Path


def get_connection():
    db_path = Path(__file__).resolve().parent.parent / "data" / "mini_data_platform.db"
    return sqlite3.connect(db_path)


def create_products_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def insert_products(products):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.executemany("""
        INSERT OR REPLACE INTO products (product_id, name, category, price)
        VALUES (?, ?, ?, ?)
    """, [
        (
            p["product_id"],
            p["name"],
            p["category"],
            p["price"]
        )
        for p in products
    ])

    connection.commit()
    connection.close()