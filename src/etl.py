import json
import requests
from pathlib import Path


def load_products():
    file_path = Path(__file__).resolve().parent.parent / "data" / "products.json"

    with open(file_path, "r", encoding="utf-8") as file:
        products = json.load(file)

    return products


def clean_products(products):
    cleaned = []

    for p in products:
        if p["price"] is None:
            continue

        cleaned_product = {
            "product_id": p["product_id"],
            "name": p["name"].strip(),
            "category": p["category"].lower(),
            "price": float(p["price"]),
        }

        cleaned.append(cleaned_product)

    return cleaned

def save_cleaned_products(products):
    file_path = Path(__file__).resolve().parent.parent / "data" / "cleaned_products.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=2)

def fetch_products_from_api():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch products: {response.status_code}")
        return []
        