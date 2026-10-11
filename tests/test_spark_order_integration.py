from spark.jobs.order_analysis import (
    validate_orders,
    validate_products,
    validate_users,
    validate_references,
    enrich_orders,
    calculate_revenue_by_category,
)

from spark.schemas.schemas import (
    orders_schema,
    products_schema,
    users_schema,
)

def test_order_analysis_pipeline(spark):
    # Create sample data for orders, products, and users
    orders = spark.createDataFrame(
        [
            ("2026-01-01", 1, 10, 2, 100),
            ("2026-01-02", 2, 20, 1, 200),
        ],
        schema=orders_schema
    )

    products = spark.createDataFrame(
        [
            ("electronics", "keyboard", 50.0, 10, 10, 4.5),
            ("electronics", "mouse", 30.0, 20, 20, 4.0),
        ],
        schema=products_schema
    )

    users = spark.createDataFrame(
        [
            ("Rotterdam", "mary@domain.com", "Mary", "123", "Rhoon", 100, "300AA"),
            ("Amsterdam", "john@domain.com", "John", "456", "Zuid", 200, "300BB"),
        ],
        schema=users_schema
    )      

    # Validate the data
    validate_orders(orders)
    validate_products(products)
    validate_users(users)   
    validate_references(orders, products, users)

    enricched = enrich_orders(orders, products, users)
    revenue = calculate_revenue_by_category(enricched).collect()

    assert enricched.count() == 2
    assert revenue[0]["category"] == "electronics"
    assert revenue[0]["total_revenue"] == 130.0  # (2*50) + (1*30)