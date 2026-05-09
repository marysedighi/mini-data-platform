from etl import fetch_products_from_api, clean_products, save_cleaned_products

def main():
    products = fetch_products_from_api()
    cleaned_products = clean_products(products)
    save_cleaned_products(cleaned_products)

    print("Original products:")
    print(products)
    print("Cleaned products:")
    print(cleaned_products)
    print("Cleaned products saved to cleaned_products.json successfully.")

if __name__ == "__main__":    
    main()