from src.etl import clean_products


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