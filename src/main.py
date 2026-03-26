from etl import load_products, clean_products

def main():
    products = load_products()
    cleaned_products = clean_products(products)

    print("Original products:")
    print(products)
    print("Cleaned products:")
    print(cleaned_products)

if __name__ == "__main__":    
    main()