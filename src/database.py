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

def create_users_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT,
            street TEXT,
            zipcode TEXT,
            phone TEXT
        )
    """)

    connection.commit()
    connection.close()

def insert_users(users):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.executemany("""
        INSERT OR REPLACE INTO users (user_id, name, email, city, street, zipcode, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            u["user_id"],
            u["name"],
            u["email"],
            u["city"],
            u["street"],
            u["zipcode"],
            u["phone"]
        )
        for u in users
    ])

    connection.commit()
    connection.close()  

def create_orders_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            order_date TEXT,
            PRIMARY KEY (oreder_id, product_id)
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    connection.commit()
    connection.close()

def insert_orders(orders):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.executemany("""
        INSERT OR REPLACE INTO orders (
                       order_id, 
                       user_id, 
                       product_id, 
                       quantity, 
                       order_date)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (
            o["order_id"],
            o["user_id"],
            o["product_id"],
            o["quantity"],
            o["order_date"]
        )
        for o in orders
    ])

    connection.commit()
    connection.close()