from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db_connection
from functools import wraps
from utils.auth import login_required



auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        phone_no = request.form.get("phone_no")  # optional
        address = request.form.get("address")    # optional

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO users (name, email, password, phone_no, address)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, email, password, phone_no, address)
        )

        db.commit()
        cursor.close()
        db.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    user = None  # initialize user

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            flash("Login successful!", "success")

            if user["role"] == "admin":
                return redirect("/admin")
            else:
                return redirect("/home")

        flash("Invalid email or password", "error")
        return redirect(url_for("auth.login"))

    # For GET requests, just render login page
    return render_template("auth/login.html")




# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
   




