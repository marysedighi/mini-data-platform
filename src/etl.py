import json
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