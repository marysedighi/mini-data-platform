from urllib import response

from src.api import (get_product_details, get_top_rated_products_endpoint, analytics_summary, health_check, get_top_users)

def test_health_check():
    response = health_check()
    assert response["status"] == "ok"

    assert response["redis"] in ["connected", "not connected"]

def test_analytics_summary():
    response = analytics_summary()
    assert "product_count" in response
    assert "revenue_per_category" in response

def test_get_top_rated_products_endpoint():
    response = get_top_rated_products_endpoint()
    assert isinstance(response, list)
    for product in response:
        assert "product_id" in product
        assert "name" in product
        assert "price" in product
        assert "rating_score" in product

def test_get_product_details_not_found():
    # Test with an invalid product_id
    response = get_product_details(9999)
    assert response == {"error": "Product not found"}

def test_get_top_users():
    response = get_top_users()

    assert isinstance(response, list)

    for user in response:
        assert "user_id" in user
        assert "name" in user
        assert "order_count" in user

        assert isinstance(user["user_id"], int)
        assert isinstance(user["name"], str)
        assert isinstance(user["order_count"], int)