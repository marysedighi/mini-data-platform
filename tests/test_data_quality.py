from src.data_quality import check_null_products, check_duplicate_products, check_null_users, check_duplicate_users, check_orders_with_invalid_references

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