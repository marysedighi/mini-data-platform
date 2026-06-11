from src.etl import fetch_orders_from_api, fetch_products_from_api, clean_products, fetch_users_from_api, save_cleaned_products
from src.database import create_products_table, insert_products
from src.analytics import(get_product_count, 
                get_average_price, get_products_per_category, get_products_with_high_rating, get_top_expensive_products, 
                get_products_above_price, get_price_segmentation, get_category_price_summary, get_ranked_products_by_price, 
                get_top_rated_products)

def main():

    products = fetch_products_from_api()
    users = fetch_users_from_api()
    orders = fetch_orders_from_api()

    cleaned_products = clean_products(products)

    # Save cleaned products to JSON file for debugging and backup
    save_cleaned_products(cleaned_products)
    
    # Create products table in SQLite database
    print("Create products table in DB")
    create_products_table()

    print("Insert cleaned products in DB")
    insert_products(cleaned_products)   

    print("Cleaned products saved to database successfully.")

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