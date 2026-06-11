from src.analytics import (get_product_count, 
                            get_average_price,
                            get_products_per_category,
                            get_price_segmentation)

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