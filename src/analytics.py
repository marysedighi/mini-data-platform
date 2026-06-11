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