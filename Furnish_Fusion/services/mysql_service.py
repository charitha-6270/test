from database.db import get_db_connection

def get_all_products():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return products


def get_products_by_category(category):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM products WHERE category=%s",
        (category,)
    )
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return products


def add_product(name, category, price, image):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, price, image) VALUES (%s, %s, %s, %s)",
        (name, category, price, image)
    )
    db.commit()
    cursor.close()
    db.close()


def delete_product(product_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    db.commit()
    cursor.close()
    db.close()
