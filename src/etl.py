import json
from urllib import response
import requests
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            "product_id": p["id"],
            "name": p["title"].strip(),
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

    try:
        logger.info(f"Fetching products from API: {url}")

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        logger.info("Products fetched successfully from API.")

        return response.json()
    
    except requests.RequestException as e:
        logger.error(f"Error fetching products from API: {e}")

        return []
        