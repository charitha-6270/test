from flask import session, redirect
from functools import wraps

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            return redirect("/home")
        return f(*args, **kwargs)
    return wrapper

