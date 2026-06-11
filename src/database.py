import sqlite3
from pathlib import Path

# create connection to the SQLite database
def get_connection():
    db_path = Path(__file__).resolve().parent.parent / "data" / "mini_data_platform.db"
    return sqlite3.connect(db_path)


def create_products_table():
    
    #open a connection to the database
    connection = get_connection()
    
    # cursor is used to execute SQL queries
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            rating_score REAL,
            rating_count INTEGER
        )
    """)

    # save changes
    connection.commit()
    connection.close()

# insert clean products into the products table
def insert_products(products):
    connection = get_connection()
    cursor = connection.cursor()# used to execute SQL queries

    # insert multiple rows 
    cursor.executemany("""
        INSERT OR REPLACE INTO products (product_id, name, category, price, rating_score, rating_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (
            p["product_id"],
            p["name"],
            p["category"],
            p["price"],
            p["rating_score"],
            p["rating_count"]
        )
        for p in products
    ])

    connection.commit()
    connection.close()