from src.analytics import (get_product_count, 
                            get_average_price,
                            get_products_per_category,
                            get_price_segmentation,
                            get_category_price_summary,
                            get_ranked_products_by_price)

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
