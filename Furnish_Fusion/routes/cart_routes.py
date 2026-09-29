from flask import Blueprint, redirect, session, render_template, url_for
from database.db import get_db_connection
from routes.auth_routes import login_required

cart_bp = Blueprint("cart", __name__)

# -------- ADD TO CART --------
@cart_bp.route("/add-to-cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Check if already in cart
    cursor.execute(
        "SELECT * FROM cart WHERE user_id=%s AND product_id=%s",
        (session["user_id"], product_id)
    )
    item = cursor.fetchone()

    if item:
        cursor.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE id=%s",
            (item["id"],)
        )
    else:
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, 1)",
            (session["user_id"], product_id)
        )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("cart.view_cart"))


# -------- VIEW CART --------
@cart_bp.route("/cart")
@login_required
def view_cart():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT cart.id, products.name, products.price, cart.quantity, products.image
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """, (session["user_id"],))

    items = cursor.fetchall()

    total = sum(item["price"] * item["quantity"] for item in items)

    cursor.close()
    db.close()

    return render_template("cart/cart.html", items=items, total=total)


# -------- REMOVE FROM CART --------
@cart_bp.route("/remove-from-cart/<int:cart_id>")
@login_required
def remove_from_cart(cart_id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM cart WHERE id=%s", (cart_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("cart.view_cart"))
