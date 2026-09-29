# LOCAL MOCK VERSION (NO AWS)

import uuid

USERS = []
PRODUCTS = [
    {"product_id": str(uuid.uuid4()), "category": "sofa", "name": "Luxury Sofa", "price": 42000, "image_url": "/static/images/sofas/sofa1.jpg"},
    {"product_id": str(uuid.uuid4()), "category": "sofa", "name": "Classic Sofa", "price": 36500, "image_url": "/static/images/sofas/sofa2.jpg"},

    {"product_id": str(uuid.uuid4()), "category": "bed", "name": "King Size Bed", "price": 55000, "image_url": "/static/images/beds/bed1.jpg"},
    {"product_id": str(uuid.uuid4()), "category": "bed", "name": "Queen Bed", "price": 48000, "image_url": "/static/images/beds/bed2.jpg"},

    {"product_id": str(uuid.uuid4()), "category": "table", "name": "Dining Table", "price": 32000, "image_url": "/static/images/tables/table1.jpg"},
    {"product_id": str(uuid.uuid4()), "category": "table", "name": "Coffee Table", "price": 18000, "image_url": "/static/images/tables/table2.jpg"},

    {"product_id": str(uuid.uuid4()), "category": "chair", "name": "Office Chair", "price": 15000, "image_url": "/static/images/chairs/chair1.jpg"},
    {"product_id": str(uuid.uuid4()), "category": "chair", "name": "Lounge Chair", "price": 22000, "image_url": "/static/images/chairs/chair2.jpg"},
]

def create_user(name, email, password):
    USERS.append({"name": name, "email": email, "password": password})

def get_user_by_email(email):
    for user in USERS:
        if user["email"] == email:
            return user
    return None

def get_products_by_category(category):
    return [p for p in PRODUCTS if p["category"] == category]

