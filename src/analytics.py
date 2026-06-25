from src.database import get_connection

def get_product_count():
    connection = get_connection()
    cursor = connection.cursor() # used to execute SQL queries

    cursor.execute("SELECT COUNT(*) FROM products")
    result = cursor.fetchone()[0] # retrieves the first row of the result set and gets the first column (the count)

    connection.close()

    return result if result else 0

def get_average_price():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT AVG(price) FROM products")
    result = cursor.fetchone()[0]

    connection.close()

    return round(result, 2) if result else 0.0

def get_products_per_category():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT category, COUNT(*) as count
        FROM products
        GROUP BY category
        ORDER BY count(*) DESC
    """)

    result = cursor.fetchall() # retrieves all rows of the result set

    connection.close()

    return result if result else []

def get_top_expensive_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        Select product_id, name, price
        From products
        Order By price DESC
        limit 5
    """)

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_products_above_price(min_price):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        Select product_id, name, price
        From products
        Where price > ?
        Order By price DESC
    """, (min_price,)
    )

    result = cursor.fetchall()

    connection.close()
    
    return result if result else []

def get_price_segmentation():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 
            CASE 
                WHEN price < 50 THEN 'Low'
                WHEN price BETWEEN 50 AND 200 THEN 'Medium'
                ELSE 'High'
            END AS price_segment,
            COUNT(*) as product_count
        FROM products
        GROUP BY price_segment
        order by product_count DESC
    """)

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_category_price_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        with category_summary as (
        SELECT category, COUNT(*) as product_count, AVG(price) as avg_price, MIN(price) as min_price, MAX(price) as max_price
        FROM products
        GROUP BY category
        )
        SELECT category, product_count, ROUND(avg_price, 2) as avg_price, min_price, max_price
        FROM category_summary
        ORDER BY avg_price DESC
    """)

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_ranked_products_by_price():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT product_id, name, price, category,
        RANK() OVER (Partition by category ORDER BY price DESC) as price_rank
        FROM products
        ORDER by category, price_rank
    """)

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_products_with_high_rating(min_rating):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT product_id, name, price, rating_score
        FROM products
        WHERE rating_score >= ?
        ORDER BY rating_score DESC
    """, (min_rating,)
    )

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_top_rated_products(limit=5):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT product_id, name, price, rating_score
        FROM products
        ORDER BY rating_score DESC
        LIMIT ?
    """, (limit,)
    )

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_orders_with_user_and_product_details():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT o.order_id, o.user_id, u.name as user_name, o.product_id, p.name as product_name,p.price as product_price, o.quantity, o.order_date
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        JOIN products p ON o.product_id = p.product_id
        ORDER BY o.order_date DESC
    """)

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_revenue_per_category():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT p.category, ROUND(SUM(o.quantity * p.price), 2) as total_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """)

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_top_users_by_order_count(limit):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT u.user_id, u.name, COUNT(DISTINCT o.order_id) as order_count
        FROM users u
        JOIN orders o ON u.user_id = o.user_id
        GROUP BY u.user_id, u.name
        ORDER BY order_count DESC
        LIMIT ?
    """, (limit,)
    )

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_top_products_by_quantity_purchased(limit=5):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT p.product_id, p.name, SUM(o.quantity) as total_quantity
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.product_id, p.name
        ORDER BY total_quantity DESC
        LIMIT ?
    """, (limit,))

    result = cursor.fetchall()

    connection.close()

    return result if result else []

def get_highest_rated_products_per_category():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT category, product_id, name, rating_score
        FROM (
            SELECT category, product_id, name, rating_score,
            RANK() OVER (PARTITION BY category ORDER BY rating_score DESC) as rank
            FROM products
        )
        WHERE rank = 1
        ORDER BY category
    """)        

    result = cursor.fetchall()
    
    connection.close()

    return result if result else []