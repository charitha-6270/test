from flask import Blueprint, session, redirect, render_template, request, flash
from database.db import get_db_connection
from routes.auth_routes import login_required
from services.sns_service import send_order_notification

order_bp = Blueprint("order", __name__)

# -------------------------------------------------
# SHOW PAYMENT PAGE
# -------------------------------------------------
@order_bp.route("/place-order")
@login_required
def place_order():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.product_id, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (session["user_id"],))

    cart_items = cursor.fetchall()

    if not cart_items:
        cursor.close()
        db.close()
        flash("Your cart is empty", "warning")
        return redirect("/cart")

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    cursor.close()
    db.close()

    return render_template("payment.html", total=total_price)


# -------------------------------------------------
# PROCESS PAYMENT & CREATE ORDER
# -------------------------------------------------
@order_bp.route("/process-payment", methods=["POST"])
@login_required
def process_payment():
    payment_method = request.form.get("payment_method")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.product_id, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (session["user_id"],))

    cart_items = cursor.fetchall()

    if not cart_items:
        cursor.close()
        db.close()
        flash("Your cart is empty", "warning")
        return redirect("/home")

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    # Create order
    cursor.execute("""
        INSERT INTO orders 
        (user_id, total_price, payment_method, payment_status, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        session["user_id"],
        total_price,
        payment_method,
        "SUCCESS",
        "paid"
    ))
    db.commit()

    order_id = cursor.lastrowid

    # Insert order items
    for item in cart_items:
        cursor.execute("""
            INSERT INTO order_items 
            (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (
            order_id,
            item["product_id"],
            item["quantity"],
            item["price"]
        ))

    db.commit()

    # Clear cart
    cursor.execute("DELETE FROM cart WHERE user_id = %s", (session["user_id"],))
    db.commit()

    cursor.close()
    db.close()

    # Notification (optional service)
    send_order_notification(order_id, total_price)

    flash("Order placed successfully 🎉", "success")
    return render_template(
        "orders/confirmation.html",
        order_id=order_id,
        total_price=total_price,
        payment_method=payment_method
    )


# -------------------------------------------------
# USER ORDER HISTORY
# -------------------------------------------------
@order_bp.route("/my-orders")
@login_required
def my_orders():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get all orders
    cursor.execute("""
        SELECT *
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (session["user_id"],))
    orders = cursor.fetchall()  # ✅ parentheses here

    # Fetch products for each order
    for order in orders:
        cursor.execute("""
            SELECT p.name, p.image, oi.quantity
            FROM order_items oi
            JOIN products p ON p.id = oi.product_id
            WHERE oi.order_id = %s
        """, (order['id'],))
        order['items'] = cursor.fetchall()  # ✅ must call fetchall()

    cursor.close()
    db.close()

    return render_template("orders/history.html", orders=orders)



# -------------------------------------------------
# CANCEL ORDER
# -------------------------------------------------
# -------------------------------------------------
# CANCEL ORDER
# -------------------------------------------------
@order_bp.route("/cancel-order/<int:order_id>")
@login_required
def cancel_order(order_id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = 'cancelled'
        WHERE id = %s 
          AND user_id = %s 
          AND status IN ('placed', 'paid')  
    """, (order_id, session["user_id"]))

    db.commit()
    cursor.close()
    db.close()

    flash("Order cancelled successfully", "info")
    return redirect("/my-orders")

# -------------------------------------------------
# RETURN ORDER
# -------------------------------------------------
@order_bp.route("/return-order/<int:order_id>")
@login_required
def return_order(order_id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = 'returned'
        WHERE id = %s 
          AND user_id = %s 
          AND status = 'delivered'
    """, (order_id, session["user_id"]))

    db.commit()
    cursor.close()
    db.close()

    flash("Return request submitted", "info")
    return redirect("/my-orders")

