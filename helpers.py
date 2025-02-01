from flask import render_template, jsonify, redirect, render_template, session
from functools import wraps

def apology(message, code):
    if code == 'login':
        return render_template("templogin.html", message=message)
    if code == 'register':
        return render_template("tempregister.html", message=message)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function