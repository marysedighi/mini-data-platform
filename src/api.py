from fastapi import FastAPI
from src.cache import check_connection

from src.analytics import get_product_count, get_products_by_id, get_revenue_per_category, get_top_rated_products, get_top_users_by_order_count

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok",
            "redis" : "connected" if check_connection() else "not connected"}


@app.get("/analytics/summary")
def analytics_summary():

    return {
        "product_count": get_product_count(),
        "revenue_per_category": get_revenue_per_category()
    }


@app.get("/top_rated_products")
def get_top_rated_products_endpoint():
    products = get_top_rated_products()
    return [
        {
            "product_id": product[0],
            "name": product[1],
            "price": product[2],
            "rating_score": product[3]
        }
        for product in products
    ]


@app.get("/products/{product_id}")
def get_product_details(product_id: int):
    product = get_products_by_id(product_id)
    if product:
        return {
            "product_id": product[0],
            "name": product[1],
            "price": product[2],
            "rating_score": product[3]
        }
    else:
        return {"error": "Product not found"}
    

@app.get("/analytics/top-users")
def get_top_users():
    users = get_top_users_by_order_count(5)
    return [
        {
            "user_id": user[0],
            "name": user[1],
            "order_count": user[2]
        }
        for user in users
    ]
