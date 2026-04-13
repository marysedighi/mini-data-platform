from src.etl import clean_products


def test_clean_products_removes_none_price():
    products = [
        {"product_id": 1, "name": "Shoes", "category": "Shoes", "price": 79.99},
        {"product_id": 2, "name": "Hat", "category": "Accessories", "price": None},
    ]

    result = clean_products(products)

    assert len(result) == 1
    assert result[0]["product_id"] == 1


def test_clean_products_strips_name():
    products = [
        {"product_id": 1, "name": "  Running Shoes  ", "category": "Shoes", "price": 79.99},
    ]

    result = clean_products(products)

    assert result[0]["name"] == "Running Shoes"


def test_clean_products_lowercases_category():
    products = [
        {"product_id": 1, "name": "Shoes", "category": "SHOES", "price": 79.99},
    ]

    result = clean_products(products)

    assert result[0]["category"] == "shoes"


def test_clean_products_converts_price_to_float():
    products = [
        {"product_id": 1, "name": "Shoes", "category": "Shoes", "price": "79.99"},
    ]

    result = clean_products(products)

    assert result[0]["price"] == 79.99
    assert isinstance(result[0]["price"], float)