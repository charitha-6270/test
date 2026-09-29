from config import SECRET_KEY
from flask import Flask, render_template


# Import routes
from routes.auth_routes import auth_bp
from routes.auth_routes import login_required


from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(admin_bp)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)
