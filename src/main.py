from etl import fetch_products_from_api, clean_products, save_cleaned_products
from database import create_products_table, insert_products
from analytics import get_product_count, get_average_price, get_products_per_category, get_top_expensive_products

def main():

    products = fetch_products_from_api()

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


if __name__ == "__main__":    
    main()