import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session
from helpers import login_required
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "study.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
@login_required
def index():
    connection = get_db_connection()
    categories = connection.execute("SELECT * FROM categories WHERE user_id = ?", (session["user_id"],)).fetchall()
    connection.close()
    return render_template("index.html", categories=categories)

@app.route("/select-category", methods=["GET", "POST"])
@login_required
def select_category():
    data = request.get_json()
    category_id = data["category_id"]
    user_id = session["user_id"]

    connection = get_db_connection()
    category = connection.execute("SELECT * FROM categories WHERE id = ? AND user_id = ?", (category_id, user_id)).fetchone()
    connection.close()
    
    if category is None:
        return {"success": False}
    
    session["selected_category"] = category_id
    return {"success": True}

@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    if request.method == "POST":
        category = request.form.get("category")
        connection = get_db_connection()
        connection.execute("INSERT INTO categories (user_id, category_name) VALUES (?, ?)", (session["user_id"], category))
        connection.commit()
        connection.close()

    connection = get_db_connection()
    categories = connection.execute("SELECT * FROM categories WHERE user_id = ?", (session["user_id"],)).fetchall()
    return render_template("categories.html", categories = categories)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    if request.method == "POST":
        id = request.form.get("id")
        connection = get_db_connection()
        connection.execute("DELETE FROM categories WHERE id = ?", (id,))
        connection.commit()
        connection.close()
        return redirect("/categories")

@app.route("/goupdate", methods=["GET", "POST"])
@login_required
def goupdate():
    if request.method == "POST":
        id = request.form.get("id")
        new_name = request.form.get("update")
        connection = get_db_connection()
        connection.execute("UPDATE categories SET category_name = ? WHERE id = ?", (new_name, id))
        connection.commit()
        connection.close()
        return redirect("/categories")

    category_id = request.args.get("id")
    return render_template("goupdate.html", id=category_id)
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password:
            flash("Enter a username and password")
            return redirect("/register")
        
        connection = get_db_connection()
        check = connection.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        if len(check) > 0 :
            connection.close()
            flash("Please choose a different username")
            return redirect("/register")

        if password != confirmation:
            flash("Please enter the same password twice")
            return redirect("/register")

        connection.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, generate_password_hash(password)))
        connection.commit()
        connection.close()

        return render_template("login.html")

    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Please enter a username")
            return redirect("/login")

        password = request.form.get("password")
        if not password:
            flash("Please enter a password")
            return redirect("/login")

        connection = get_db_connection()
        user = connection.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        connection.close()

        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            flash("Please enter a valid username or password")
            return redirect("/login")

        session["user_id"] = user[0]["id"]
        print("Logged in")
        return redirect("/")

    
    return render_template("login.html")

#Took this one straight from cs50
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")