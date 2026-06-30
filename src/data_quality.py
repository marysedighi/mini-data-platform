from src.database import get_connection


def check_null_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM products WHERE product_id IS NULL OR name IS NULL OR category IS NULL OR price IS NULL")
    
    result = cursor.fetchone()[0]

    connection.close()

    return result

def check_duplicate_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, COUNT(*)
        FROM products
        GROUP BY product_id
        HAVING COUNT(*) > 1
    """)

    result = cursor.fetchall()

    connection.close()

    return result

def check_null_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id IS NULL OR name IS NULL OR email IS NULL")
    
    result = cursor.fetchone()[0]

    connection.close()

    return result

def check_duplicate_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_id, COUNT(*)
        FROM users
        GROUP BY user_id
        HAVING COUNT(*) > 1
    """)

    result = cursor.fetchall()

    connection.close()

    return result

def check_row_counts():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    connection.close()

    return {"products": product_count,
             "users": user_count, 
             "orders": order_count
        }

def check_orders_with_invalid_references():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT o.order_id, o.user_id, o.product_id
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.user_id
        LEFT JOIN products p ON o.product_id = p.product_id
        WHERE u.user_id IS NULL OR p.product_id IS NULL
    """)

    result = cursor.fetchall()

    connection.close()

    return result