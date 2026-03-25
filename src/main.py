import json
from pathlib import Path

def load_products():
    file_path = Path(__file__).resolve().parent.parent / "data" / "products.json"

    with open(file_path, "r", encoding="utf-8") as file:
        products = json.load(file)

    return products

def main():
    products = load_products()
    print("Loaded products:")
    print(products)

if __name__ == "__main__":    main()