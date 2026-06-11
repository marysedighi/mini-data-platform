import json
from urllib import response
import requests
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch products from API with error handling and fallback to local file
def fetch_products_from_api():
    url = "https://fakestoreapi.com/products"

    try:
        logger.info(f"Fetching products from API: {url}")

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        logger.info("Products fetched successfully from API.")

        return response.json()
    
    # Fallback to local file if API is unavailable
    except requests.RequestException as e:
        logger.error(f"Error fetching products from API: {e}")
        logger.info("Falling back to local products.json file.")
        
        return load_products()
    
# load data from local JSON file as fallback
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
            "rating_score": float(p["rating"]["rate"]),
            "rating_count": int(p["rating"]["count"])
        }

        cleaned.append(cleaned_product)

    return cleaned

# Save cleaned products to a JSON file for debugging and backup
def save_cleaned_products(products):
    file_path = Path(__file__).resolve().parent.parent / "data" / "cleaned_products.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=2)


def fetch_users_from_api():
    url = "https://fakestoreapi.com/users"

    try:
        logger.info(f"Fetching users from API: {url}")

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        logger.info("Users fetched successfully from API.")

        return response.json()
    
    except requests.RequestException as e:
        logger.error(f"Error fetching users from API: {e}")
        return []
    
def clean_users(users):
    cleaned = []

    for u in users:
        cleaned_user = {
            "user_id": u["id"],
            "name": f"{u['name']['firstname']} {u['name']['lastname']}".strip(),
            "email": u["email"].lower(),
            "city": u["address"]["city"].lower(),
            "street": u["address"]["street"].lower(),
            "zipcode": u["address"]["zipcode"].lower(),
            "phone": u["phone"].strip()
        }

        cleaned.append(cleaned_user)

    return cleaned

def save_cleaned_users(users):
    file_path = Path(__file__).resolve().parent.parent / "data" / "cleaned_users.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)
    
def fetch_orders_from_api():
    url = "https://fakestoreapi.com/carts"

    try:
        logger.info(f"Fetching orders from API: {url}")

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        logger.info("Orders fetched successfully from API.")

        return response.json()
    
    except requests.RequestException as e:
        logger.error(f"Error fetching orders from API: {e}")
        return []
    
def clean_orders(orders):
    cleaned = []

    for o in orders:
        for p in o["products"]:
            cleaned_order_item = {
                "order_id": o["id"],
                "user_id": o["userId"],
                "order_date": o["date"],
                "product_id": p["productId"],
                "quantity": p["quantity"]
            }

        cleaned.append(cleaned_order_item)

    return cleaned

def save_cleaned_orders(orders):
    file_path = Path(__file__).resolve().parent.parent / "data" / "cleaned_orders.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=2)