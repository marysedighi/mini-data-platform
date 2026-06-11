from src.etl import (fetch_orders_from_api, fetch_products_from_api,
                clean_products, fetch_users_from_api, save_cleaned_products,
                clean_users, clean_orders, save_cleaned_users, save_cleaned_orders)

from src.database import (create_orders_table, create_products_table, create_users_table,
                insert_orders, insert_products, insert_users)

from src.analytics import(get_product_count, 
                get_average_price, get_products_per_category, get_products_with_high_rating, get_top_expensive_products, 
                get_products_above_price, get_price_segmentation, get_category_price_summary, get_ranked_products_by_price, 
                get_top_rated_products)


def main():

    # fetch, clean, and load products, users and orders data into the DB file
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

    # Run analytics queries and print results 

    print(f"Product count: {get_product_count()}")
    print(f"Average price: ${get_average_price()}")

    print("Products per category:")
    print(get_products_per_category())

    print("Top expensive products:")
    print(get_top_expensive_products())

    print("Products above $100:")
    print(get_products_above_price(100))

    print("Price segmentation:")
    print(get_price_segmentation())

    print("Category price summary:")
    print(get_category_price_summary())

    print("Ranked products by price:")
    print(get_ranked_products_by_price())

    print("Products with high rating (>= 4.0):")
    print(get_products_with_high_rating(4.0))

    print("5 top rated products:")
    print(get_top_rated_products(5))
    
if __name__ == "__main__":    
    main()