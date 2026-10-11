import pytest
from spark.jobs.order_analysis import (
    enrich_orders,
    validate_orders,
    validate_products,
    validate_users,
    validate_references,
    calculate_revenue_by_category,
    calculate_top_users,
    calculate_top_products
)

from spark.schemas.schemas import (
    orders_schema,
    products_schema,
    users_schema
)

def test_enrich_orders(spark):
    orders = spark.createDataFrame(
        [
            ("2026-01-01", 1, 10, 2, 100),
        ], 
        schema=orders_schema
    )   

    products = spark.createDataFrame(
        [
            ("electronics", "keyboard", 50.0, 10, 10, 4.5),
        ], 
        schema=products_schema
    )

    users = spark.createDataFrame(
        [
            ("Rotterdam", "mary@domain.com", "Mary", "123", "Rhoon", 100, "300AA"),
        ], 
        schema=users_schema
    )

    result = enrich_orders(orders, products, users)        

    row = result.collect()[0]

    assert row.product_name == "keyboard"
    assert row.user_name == "Mary"
    assert row.total_price == pytest.approx(100.0)


def test_validate_orders_rejects_zero_quantity(spark):
    orders = spark.createDataFrame(
        [
            ("2026-01-01", 1, 10, 0, 100),
        ], 
        schema=orders_schema
    )   

    with pytest.raises(ValueError, match="Invalid orders found"):
        validate_orders(orders)

def test_validate_refrences_rejects_unknown_product(spark):
    orders = spark.createDataFrame(
        [
            ("2026-01-01", 1, 99, 2, 100),
        ], 
        schema=orders_schema
    )   

    products = spark.createDataFrame(
        [
            ("electronics", "keyboard", 50.0, 11, 10, 4.5),
        ], 
        schema=products_schema
    )

    users = spark.createDataFrame(
        [
            ("Rotterdam", "mary@domain.com", "Mary", "123", "Rhoon", 100, "300AA"),
        ], 
        schema=users_schema
    )


    with pytest.raises(ValueError, match="Orders reference unknown products"):
        validate_references(orders, products, users)

def test_calculate_revenue_by_category(spark): 
    data = [
        (1, 100, 10, "2026-01-01", 2, "keyboard", "electronics", 50.0, "Mary", 100.0),
        (2, 200, 20, "2026-01-02", 3, "mouse", "electronics", 25.0, "John", 50.0),
    ]

    columns = [
        "order_id", 
        "user_id", 
        "product_id", 
        "order_date", 
        "quantity", 
        "product_name", 
        "category", 
        "price", 
        "user_name", 
        "total_price"]

    df = spark.createDataFrame(data, columns)

    result = calculate_revenue_by_category(df).collect()

    assert result[0]["category"] == "electronics"
    assert result[0]["total_revenue"] == pytest.approx(150.0)


def test_calculate_top_users(spark):
    data = [
        (1, 100, 10, "2026-01-01", 2, "keyboard", "electronics", 50.0, "Mary", 100.0),
        (2, 200, 20, "2026-01-02", 3, "mouse", "electronics", 25.0, "John", 50.0),
        (3, 100, 30, "2026-01-03", 1, "monitor", "electronics", 150.0, "Mary", 150.0),
    ]

    columns = [
        "order_id", 
        "user_id", 
        "product_id", 
        "order_date", 
        "quantity", 
        "product_name", 
        "category", 
        "price", 
        "user_name", 
        "total_price"]

    df = spark.createDataFrame(data, columns)

    result = calculate_top_users(df).collect()

    assert result[0]["user_name"] == "Mary"
    assert result[0]["total_spent"] == pytest.approx(250.0)


def test_calculate_top_products(spark):
    data = [
        (1, 100, 10, "2026-01-01", 2, "keyboard", "electronics", 50.0, "Mary", 100.0),
        (2, 200, 20, "2026-01-02", 3, "mouse", "electronics", 25.0, "John", 75.0),
        (3, 300, 10, "2026-01-03", 1, "keyboard", "electronics", 50.0, "Alice", 50.0),
    ]

    columns = [
        "order_id", 
        "user_id", 
        "product_id", 
        "order_date", 
        "quantity", 
        "product_name", 
        "category", 
        "price", 
        "user_name", 
        "total_price"]

    df = spark.createDataFrame(data, columns)

    result = calculate_top_products(df).collect()

    assert result[0]["product_name"] == "keyboard"
    assert result[0]["total_revenue"] == pytest.approx(150.0)