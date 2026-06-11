from src.database import create_products_table, insert_products, get_connection

def test_create_products_table():
    create_products_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    result = cursor.fetchone()

    connection.close()

    assert result is not None
    assert result[0] == "products"  

def test_insert_products():
    create_products_table()

    products = [
        {"product_id": 1, "name": "Shoes", "category": "Shoes", "price": 79.99, "rating_score": 4.5, "rating_count": 100},
        {"product_id": 2, "name": "Hat", "category": "Accessories", "price": 19.99, "rating_score": 4.0, "rating_count": 50},
    ]

    insert_products(products)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT product_id, name, category, price, rating_score, rating_count FROM products where product_id in (1, 2)")
    result = cursor.fetchall()

    connection.close()

    assert len(result) == 2
    assert result[0] == (1, "Shoes", "Shoes", 79.99, 4.5, 100)
    assert result[1] == (2, "Hat", "Accessories", 19.99, 4.0, 50)