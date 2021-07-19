import os
import requests
from flask_paginate import Pagination, get_page_parameter
# import json
from flask import (
    Flask, render_template, flash,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Configuration #
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    recipes = list(mongo.db.recipes.find())
    return render_template("index.html", 
                           page_title="Yummy Recipes",
                           recipes=recipes)


@app.route("/about")
def about():
    return render_template("about.html", page_title="About Us")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact Us")


@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html", page_title="Accessibility")


@app.route("/terms")
def terms():
    return render_template("terms.html", page_title="Terms of Use & Policies")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", page_title="Privacy Policy")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html", page_title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html", page_title="Log In")


@ app.route('/logout')
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for('login'))


# User profile page #
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Retrieve users and recipes to use on profile page #
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    users = list(mongo.db.users.find())
    recipes = list(mongo.db.recipes.find())
    favourite_recipes = mongo.db.users.find_one(
                {"username": session["user"]})["favourite_recipes"]
    # Favourite recipe display functionality advised by CI tutors #
    favourites = []
    # To push to favourites array #
    for recipe in favourite_recipes:
        favourites.append(mongo.db.recipes.find_one({"_id": recipe}))
    if session["user"]:
        return render_template(
            "profile.html", username=username, users=users,
            recipes=recipes, favourites=favourites, page_title="Profile")

    return redirect(url_for("login"))


# ---- NEWSLETTER SUBSCRIPTION FORM ----- #
@ app.route('/sub', methods=['POST'])
def sub():
    sub = mongo.db.newsletter
    return_data = request.form.to_dict()
    sub.insert_one(return_data)
    flash("Sucessfully Subscribed")
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
