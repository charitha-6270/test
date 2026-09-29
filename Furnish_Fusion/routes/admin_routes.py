from flask import Blueprint, render_template, request, redirect, url_for
from database.db import get_db_connection
from services.authguard import admin_required

admin_bp = Blueprint("admin", __name__)

# ---------------- DASHBOARD ----------------
@admin_bp.route("/admin")
@admin_required
def dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("admin/dashboard.html", products=products)

# ---------------- ADD PRODUCT ----------------
@admin_bp.route("/admin/add", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO products (name, category, price, image)
            VALUES (%s, %s, %s, %s)
            """,
            (
                request.form["name"],
                request.form["category"],
                request.form["price"],
                request.form["image"]
            )
        )

        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_product.html")

# ---------------- EDIT PRODUCT ----------------
@admin_bp.route("/admin/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_product(id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute(
            """
            UPDATE products
            SET name=%s, category=%s, price=%s, image=%s
            WHERE id=%s
            """,
            (
                request.form["name"],
                request.form["category"],
                request.form["price"],
                request.form["image"],
                id
            )
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("admin.dashboard"))

    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cursor.fetchone()

    cursor.close()
    db.close()
    return render_template("admin/edit_product.html", product=product)

# ---------------- DELETE PRODUCT ----------------
@admin_bp.route("/admin/delete/<int:id>")
@admin_required
def delete_product(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    db.commit()

    cursor.close()
    db.close()
    return redirect(url_for("admin.dashboard"))

# ---------------- VIEW ORDERS (WITH PRODUCTS) ----------------
@admin_bp.route("/admin/orders")
@admin_required
def admin_orders():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Fetch all orders with customer name
    cursor.execute("""
        SELECT o.*, u.name AS customer_name
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()

    # Fetch items for each order
    for order in orders:
        cursor.execute("""
            SELECT p.name, p.image, oi.quantity
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """, (order['id'],))

        # ✅ VERY IMPORTANT
        order['items'] = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin/orders.html", orders=orders)


# ---------------- UPDATE ORDER STATUS ----------------
@admin_bp.route("/admin/order-status/<int:order_id>/<status>")
@admin_required
def update_order_status(order_id, status):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE orders SET status=%s WHERE id=%s",
        (status, order_id)
    )

    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("admin.admin_orders"))



