from src.etl import (fetch_orders_from_api, fetch_products_from_api,
                clean_products, fetch_users_from_api, save_cleaned_products,
                clean_users, clean_orders, save_cleaned_users, save_cleaned_orders)

from src.database import (create_orders_table, create_products_table, create_users_table,
                insert_orders, insert_products, insert_users)
 
def products_pipeline():

    # Fetch products from API and clean the data
    products = fetch_products_from_api()
    cleaned_products = clean_products(products)

    # Save cleaned products to a JSON file
    save_cleaned_products(cleaned_products)
    
    print("Create products table in DB")
    create_products_table()

    print("Insert cleaned products in DB")
    insert_products(cleaned_products)   

    print("Cleaned products saved to database successfully.")

def users_pipeline():

    # Fetch users from API and clean the data
    users = fetch_users_from_api()
    cleaned_users = clean_users(users)

    # Save cleaned users to a JSON file
    save_cleaned_users(cleaned_users)

    print("Create users table in DB")
    create_users_table()

    print("Insert cleaned users in DB")
    insert_users(cleaned_users)

    print("Cleaned users saved to database successfully.")

def orders_pipeline():

    # Fetch orders from API and clean the data 
    orders = fetch_orders_from_api()
    cleaned_orders = clean_orders(orders)

    # Save cleaned orders to a JSON file
    save_cleaned_orders(cleaned_orders)

    print("Create orders table in DB")
    create_orders_table()

    print("Insert cleaned orders in DB")
    insert_orders(cleaned_orders)

    print("Cleaned orders saved to database successfully.")