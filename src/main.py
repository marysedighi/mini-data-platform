from src.etl import (fetch_orders_from_api, fetch_products_from_api,
                clean_products, fetch_users_from_api, save_cleaned_products,
                clean_users, clean_orders, save_cleaned_users, save_cleaned_orders)

from src.database import (create_orders_table, create_products_table, create_users_table,
                insert_orders, insert_products, insert_users)

from src.analytics import(get_orders_with_user_and_product_details, get_product_count, 
                get_average_price, get_products_per_category, get_products_with_high_rating, get_revenue_per_category, get_top_expensive_products, 
                get_products_above_price, get_price_segmentation, get_category_price_summary, get_ranked_products_by_price, get_top_products_by_quantity_purchased, 
                get_top_rated_products, get_top_users_by_order_count)

from src.data_quality import check_duplicate_products, check_duplicate_users, check_null_products, check_null_users, check_orders_with_invalid_references, check_row_counts

def products_pipeline():
    products = fetch_products_from_api()
    cleaned_products = clean_products(products)
    save_cleaned_products(cleaned_products)     # Save cleaned products to a JSON file
    create_products_table()
    insert_products(cleaned_products)   # insert clean products into table(SQLite DB)

def users_pipeline():
    users = fetch_users_from_api()
    cleaned_users = clean_users(users)
    save_cleaned_users(cleaned_users) # Save cleaned users to a JSON file
    create_users_table()
    insert_users(cleaned_users) # insert clean users into table(SQLite DB)

def orders_pipeline():
    orders = fetch_orders_from_api()
    cleaned_orders = clean_orders(orders)
    save_cleaned_orders(cleaned_orders) # Save cleaned orders to a JSON file
    create_orders_table()
    insert_orders(cleaned_orders) # insert clean orders into table(SQLite DB)


def main():

    products_pipeline()
    users_pipeline()
    orders_pipeline()

    # Run quality checks functions
    print("Running quality checks...")
    print(f"Null products: {check_null_products()}")
    print(f"Duplicate products: {check_duplicate_products()}")
    print(f"Null users: {check_null_users()}")
    print(f"Duplicate users: {check_duplicate_users()}")
    print(f"Check order with invalid references: {check_orders_with_invalid_references()}")
    
    counts = check_row_counts()
    print(f"Products: {counts['products']}")
    print(f"Users: {counts['users']}")
    print(f"Orders: {counts['orders']}")

    print("Quality checks completed.")

    # Run analytics queries and print results 
    print("Running analytics queries...")

    print(f"Product count: {get_product_count()}")

    print(f"Average price: {get_average_price()}")

    print(f"Revenue per category: {get_revenue_per_category()}")

    print(f"Top expensive products: {get_top_expensive_products()}")

    print(f"Products above 100: {get_products_above_price(100)}")

    print(f"Price segmentation: {get_price_segmentation()}")

    print(f"Category price summary: {get_category_price_summary()}")

    print(f"Ranked products by price: {get_ranked_products_by_price()}")

    print(f"Products with high rating (>= 4.0): {get_products_with_high_rating(4.0)}")

    print(f"5 top rated products: {get_top_rated_products(5)}")

    print(f"Orders with user and product details: {get_orders_with_user_and_product_details()}")

    print(f"Top products by quantity purchased: {get_top_products_by_quantity_purchased(10)}")

    print(f"Top users by total order count: {get_top_users_by_order_count(10)}")

    print("Data pipeline and analytics completed successfully.")
    
if __name__ == "__main__":    
    main()