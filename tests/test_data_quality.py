from src.data_quality import (check_null_products,
                              check_duplicate_products,
                              check_null_users, 
                              check_duplicate_users, 
                              check_orders_with_invalid_references, 
                              check_row_counts
                            )

def test_null_products():
    result = check_null_products()

    assert isinstance(result, int)
    assert result == 0

def test_duplicate_products():
    result = check_duplicate_products()

    assert isinstance(result, list)
    assert len(result) == 0

def test_null_users():
    result = check_null_users()

    assert isinstance(result, int)
    assert result == 0

def test_duplicate_users():
    result = check_duplicate_users()

    assert isinstance(result, list)
    assert len(result) == 0

def test_row_counts():
    result = check_row_counts()

    assert isinstance(result, dict)
    assert "products" in result
    assert "users" in result
    assert "orders" in result


def test_orders_with_invalid_references():
    from src.database import insert_users, insert_products

    insert_users([
        {"user_id": 1, "name": "Alice", "email": "a@yahoo.com", "city": "Hamburg", "street": "isfeld", "zipcode": "55279", "phone": "676989"}
    ])

    insert_products([
        {"product_id": 1, "name": "Product A", "category": "cat", "price": 10.0, "rating_score": 4.0, "rating_count": 10},
        {"product_id": 2, "name": "Product B", "category": "cat", "price": 20.0, "rating_score": 4.5, "rating_count": 20},
    ])

    result = check_orders_with_invalid_references()

    assert isinstance(result, list)
    assert len(result) == 0