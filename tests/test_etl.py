from src.etl import clean_orders, clean_products, clean_users


def test_clean_products_removes_none_price():
    products = [
        {"id": 1, "title": "Shoes", "category": "Shoes", "price": 79.99, "rating": {"rate": 4.5, "count": 100}},
        {"id": 2, "title": "Hat", "category": "Accessories", "price": None, "rating": {"rate": 4.0, "count": 50}},
    ]

    result = clean_products(products)

    assert len(result) == 1
    assert result[0]["product_id"] == 1


def test_clean_products_strips_name():
    products = [
        {"id": 1, "title": "  Running Shoes  ", "category": "Shoes", "price": 79.99, "rating": {"rate": 4.5, "count": 100}},
    ]

    result = clean_products(products)

    assert result[0]["name"] == "Running Shoes"


def test_clean_products_lowercases_category():
    products = [
        {"id": 1, "title": "Shoes", "category": "SHOES", "price": 79.99, "rating": {"rate": 4.5, "count": 100}},
    ]

    result = clean_products(products)

    assert result[0]["category"] == "shoes"


def test_clean_products_converts_price_to_float():
    products = [
        {"id": 1, "title": "Shoes", "category": "Shoes", "price": "79.99", "rating": {"rate": 4.5, "count": 100}},
    ]

    result = clean_products(products)

    assert result[0]["price"] == 79.99
    assert isinstance(result[0]["price"], float)

def test_clean_user_strips_name():
    users = [
        {
            "id": 1,
            "email": "TEST@EMAIL.COM",
            "name": {
                "firstname": "Mary",
                "lastname": "sdgy"
            },
            "address": {
                "city": "Rotterdam",
                "street": "Main Street",
                "zipcode": "1234AB"
            },
            "phone": " 123456 "
        },
        {
            "id": 2,
            "email": "bob@example.com",
            "name": {
                "firstname": "Bob",
                "lastname": "Johnson"
            },
            "address": {
                "city": "Amsterdam",
                "street": "Second Street",
                "zipcode": "5678CD"
            },
            "phone": " 789012 "
        }
    ]

    result = clean_users(users)
    assert result[0]["name"] == "Mary sdgy"
    assert result[1]["email"] == "bob@example.com"

def test_clean_order_skips_missing_fields():
    orders = [
        {"id": 1, "userId": 1, "date": "2024-01-01", "products": [{"productId": 1, "quantity": 2}]},
        {"id": 2, "userId": 2, "date": "2024-01-02", "products": [{"productId": 2}]},  # Missing quantity
        {"id": 3, "userId": 3, "date": "2024-01-03", "products": []},  # Missing products
    ]

    result = clean_orders(orders)

    assert len(result) == 1
    assert result[0]["order_id"] == 1