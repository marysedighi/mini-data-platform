import pytest

from src.database import (
    create_orders_table, 
    create_products_table, 
    create_users_table, 
    insert_orders, 
    insert_products, 
    get_connection, 
    insert_users
)

@pytest.fixture(autouse=True)
def cleanup_database():
    create_products_table()
    create_users_table()
    create_orders_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM users")

    connection.commit()
    connection.close()

def test_create_products_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    result = cursor.fetchone()

    connection.close()

    assert result is not None
    assert result[0] == "products"  

def test_insert_products():

    products = [
        {"product_id": 1, "name": "Shoes", "category": "Shoes", "price": 79.99, "rating_score": 4.5, "rating_count": 100},
        {"product_id": 2, "name": "Hat", "category": "Accessories", "price": 19.99, "rating_score": 4.0, "rating_count": 50},
    ]

    insert_products(products)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT product_id, name, category, price, rating_score, rating_count FROM products where product_id in (1, 2) order by product_id")
    result = cursor.fetchall()

    connection.close()

    assert len(result) == 2
    assert result[0] == (1, "Shoes", "Shoes", 79.99, 4.5, 100)
    assert result[1] == (2, "Hat", "Accessories", 19.99, 4.0, 50)

def test_create_users_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()

    connection.close()

    assert result is not None
    assert result[0] == "users"

def test_insert_users():

    users = [
        {"user_id": 1, "name": "Alice", "email": "alice@example.com", "city": "New York", "street": "123 Main St", "zipcode": "10001", "phone": "555-1234"},
        {"user_id": 2, "name": "Bob", "email": "bob@example.com", "city": "Los Angeles", "street": "456 Oak Ave", "zipcode": "90210", "phone": "555-5678"}
    ]

    insert_users(users)

    connection = get_connection()
    cursor = connection.cursor()        
    
    cursor.execute("SELECT user_id, name, email, city, street, zipcode, phone FROM users where user_id in (1, 2) order by user_id")
   
    result = cursor.fetchall()
    
    connection.close()
    
    assert len(result) == 2
    assert result[0] == (1, "Alice", "alice@example.com", "New York", "123 Main St", "10001", "555-1234")

def test_create_orders_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")

    result = cursor.fetchone()

    connection.close()

    assert result is not None
    assert result[0] == "orders"

def test_insert_orders():

    orders = [
        {"order_id": 1, "user_id": 1, "product_id": 1, "quantity": 2, "order_date": "2024-01-01"},
        {"order_id": 1, "user_id": 1, "product_id": 2, "quantity": 1, "order_date": "2024-01-01"}
    ]

    insert_orders(orders)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, user_id, product_id, quantity, order_date
        FROM orders
        WHERE order_id = 1
        ORDER BY product_id
    """)
    
    result = cursor.fetchall()

    connection.close()

    assert len(result) == 2
    assert result[0] == (1, 1, 1, 2, "2024-01-01")
    assert result[1] == (1, 1, 2, 1, "2024-01-01")    