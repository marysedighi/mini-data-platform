from src.pipeline import orders_pipeline, users_pipeline, products_pipeline
from src.analytics import(get_product_count, 
                get_average_price, get_products_per_category, get_products_with_high_rating, get_top_expensive_products, 
                get_products_above_price, get_price_segmentation, get_category_price_summary, get_ranked_products_by_price, 
                get_top_rated_products)


def main():

    # Run ETL pipelines to fetch, clean, and load data into the database
    products_pipeline()
    users_pipeline()
    orders_pipeline()

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