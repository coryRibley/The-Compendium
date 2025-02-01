from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)
app.debug = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///cocktail.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    username = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["username"]

    if request.method == "POST":

        return render_template("index.html", username=username)

    if request.method == "GET":

        return render_template("index.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    code = 'login'
    session.clear()

    if request.method == "POST":
        username = request.form.get("username").lower().strip()
        password = request.form.get("password")

        if not username:
            return apology("Please input a valid username or email.", code)
        
        if not password:
            return apology("Please input a valid password.", code)
        
        if "@" in username:
            rows = db.execute(
                "SELECT * FROM users WHERE email = ?", username
            )
        else:
            rows = db.execute(
                "SELECT * FROM users WHERE username = ?", username
            )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            return apology("Your username or password is incorrect.", code)
    
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    
    else:
        return render_template("templogin.html")
        
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    code = 'register'

    if request.method == "POST":
        username = request.form.get("username").lower().strip()
        email = request.form.get("email").lower().strip()
        password = request.form.getlist("password")
        username_rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        email_rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        if not username:
            return apology("Please input a valid username.", code)
        
        if not email:
            return apology("Please input a valid email address.", code)
        
        if not password[0] or not password[1]:
            return apology("Please input a valid password.", code)
        
        if password[0] != password[1]:
            return apology("Please ensure passwords match eachother.", code)
        
        if len(username_rows) != 0:
            return apology("Username taken.", code)
        
        if len(email_rows) != 0:
            return apology("Email is already in use.", code)

        db.execute(
            "INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", 
            username, email, generate_password_hash(password[0])
            )
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    
    else:
        return render_template("tempregister.html")
        
@app.route("/deregister", methods=["GET", "POST"])
@login_required
def deregister():

    if request.method == "POST":

        action = request.form.get('action')
        if action == 'return':
            return redirect("/")

        elif action == 'delete':
            db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
            session.clear()
            return redirect("/")
    
    return render_template('deregister.html')

if __name__ == "__main__":
    app.run(debug=True)