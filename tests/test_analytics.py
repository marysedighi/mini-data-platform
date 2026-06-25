from src.analytics import (get_orders_with_user_and_product_details, get_product_count, 
                            get_average_price,
                            get_products_per_category,
                            get_price_segmentation,
                            get_category_price_summary, get_products_with_high_rating,
                            get_ranked_products_by_price, get_revenue_per_category, get_top_products_by_quantity_purchased,
                            get_top_rated_products, get_top_users_by_order_count)

def test_get_product_count():
    count = get_product_count()
    assert isinstance(count, int)
    assert count >= 0

def test_get_average_price():
    avg_price = get_average_price()
    assert isinstance(avg_price, (int, float))
    assert avg_price >= 0

def test_get_products_per_category():
    products_per_category = get_products_per_category()
    assert isinstance(products_per_category, list)
    for category, count in products_per_category:
        assert isinstance(category, str)
        assert isinstance(count, int)
        assert count >= 0

def test_get_price_segmentation():
    price_segmentation = get_price_segmentation()
    assert isinstance(price_segmentation, list)
    for segment, count in price_segmentation:
        assert isinstance(segment, str)
        assert isinstance(count, int)
        assert count >= 0

def test_get_category_price_summary():
    category_price_summary = get_category_price_summary()
    assert isinstance(category_price_summary, list)
    for category, product_count, avg_price, min_price, max_price in category_price_summary:
        assert isinstance(category, str)
        assert isinstance(product_count, int)
        assert isinstance(avg_price, (int, float))
        assert isinstance(min_price, (int, float))
        assert isinstance(max_price, (int, float))
        assert avg_price >= 0

def test_get_ranked_products_by_price():
    ranked_products = get_ranked_products_by_price()
    assert isinstance(ranked_products, list)
    for product_id, name, price,category, price_rank in ranked_products:
        assert isinstance(product_id, int)
        assert isinstance(name, str)
        assert isinstance(category, str)
        assert isinstance(price, (int, float))
        assert isinstance(price_rank, int)
        assert price >= 0

def test_get_products_with_high_rating():
    min_rating = 4.0
    products_with_high_rating = get_products_with_high_rating(min_rating)
    assert isinstance(products_with_high_rating, list)
    for product_id, name, price, rating_score in products_with_high_rating:
        assert isinstance(product_id, int)
        assert isinstance(name, str)
        assert isinstance(price, (int, float))
        assert isinstance(rating_score, (int, float))
        assert rating_score >= min_rating

def test_get_top_rated_products():
    limit = 5
    top_rated_products = get_top_rated_products(limit)
    assert isinstance(top_rated_products, list)
    assert len(top_rated_products) <= limit
    for product_id, name, price, rating_score in top_rated_products:
        assert isinstance(product_id, int)
        assert isinstance(name, str)
        assert isinstance(price, (int, float))
        assert isinstance(rating_score, (int, float))
        assert rating_score >= 0

def test_get_revenue_per_category():
    revenue_per_category = get_revenue_per_category()
    assert isinstance(revenue_per_category, list)
    for category, total_revenue in revenue_per_category:
        assert isinstance(category, str)
        assert isinstance(total_revenue, (int, float))
        assert total_revenue >= 0


def test_get_top_users_by_order_count():
    limit = 5
    top_users = get_top_users_by_order_count(limit)
    assert isinstance(top_users, list)
    assert len(top_users) <= limit
    for user_id, name, order_count in top_users:
        assert isinstance(user_id, int)
        assert isinstance(name, str)
        assert isinstance(order_count, int)
        assert order_count >= 0

def test_get_orders_with_user_and_product_details():
    orders_with_details = get_orders_with_user_and_product_details()
    assert isinstance(orders_with_details, list)
    for order_id, user_id, user_name, product_id, product_name, product_price, quantity, order_date in orders_with_details:
        assert isinstance(order_id, int)
        assert isinstance(user_id, int)
        assert isinstance(user_name, str)
        assert isinstance(product_id, int)
        assert isinstance(product_name, str)
        assert isinstance(product_price, (int, float))
        assert isinstance(quantity, int)
        assert isinstance(order_date, str)  # Assuming order_date is stored as a string in the database

def test_get_top_products_by_quantity_purchased():
    limit = 5
    top_products = get_top_products_by_quantity_purchased(limit)
    assert isinstance(top_products, list)
    assert len(top_products) <= limit
    for product_id, name, total_quantity in top_products:
        assert isinstance(product_id, int)
        assert isinstance(name, str)
        assert isinstance(total_quantity, int)
        assert total_quantity >= 0