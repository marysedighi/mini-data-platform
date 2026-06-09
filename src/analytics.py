from database import get_connection

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
