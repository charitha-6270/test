from flask import Blueprint, render_template
from database.db import get_db_connection
from routes.auth_routes import login_required
from utils.auth import login_required

product_bp = Blueprint("products", __name__)

# ---------- SOFAS ----------
@product_bp.route("/sofas")
@login_required
def sofas():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE category='sofa'")
    products = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("products/sofas.html", products=products)


# ---------- BEDS ----------
@product_bp.route("/beds")
@login_required
def beds():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE category='bed'")
    products = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("products/beds.html", products=products)


# ---------- TABLES ----------
@product_bp.route("/tables")
@login_required
def tables():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE category='table'")
    products = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("products/tables.html", products=products)


# ---------- CHAIRS ----------
@product_bp.route("/chairs")
@login_required
def chairs():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE category='chair'")
    products = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("products/chairs.html", products=products)
