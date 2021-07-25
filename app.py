import os
from flask_paginate import Pagination, get_page_parameter
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

# Pagination #
PER_PAGE = 8


def paginated(recipes, page):
    offset = page * PER_PAGE - PER_PAGE
    paginated_recipes = recipes[offset: offset + PER_PAGE]
    pagination = Pagination(page=page, per_page=PER_PAGE, total=len(recipes))
    return [
        paginated_recipes,
        pagination
    ]


# --- Public Sites --- #
# Home Page #
@app.route("/")
def index():
    # 6 random recipes #
    recipes = mongo.db.recipes
    random_recipes = (
        [recipe for recipe in recipes.aggregate([
            {"$sample": {"size": 6}}])])
    # 3 random products #
    products = mongo.db.products
    random_products = (
        [product for product in products.aggregate([
            {"$sample": {"size": 3}}])])
    return render_template("index.html",
                           page_title="Yummy Recipes",
                           recipes=recipes,
                           random_recipes=random_recipes,
                           products=products,
                           random_products=random_products)


@app.route("/article")
def article():
    return render_template("article.html", page_title="DIY Tips")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact Us")


@app.route("/about")
def about():
    return render_template("about.html", page_title="About Us")


@app.route("/advertising")
def advertising():
    return render_template("advertising.html", page_title="Advertising Policy")


@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html", page_title="Accessibility")


@app.route("/terms")
def terms():
    return render_template("terms.html", page_title="Terms of Use & Policies")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", page_title="Privacy Policy")


# Recipes Page #
@app.route("/all_recipes")
def all_recipes():
    # Get all recipes from DB #
    recipes = list(mongo.db.recipes.find().sort("_id", -1))
    # Pagination #
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination_obj = paginated(recipes, page)
    paginated_recipes = pagination_obj[0]
    pagination = pagination_obj[1]
    # 3 random products #
    products = mongo.db.products
    random_products = (
        [product for product in products.aggregate([
            {"$sample": {"size": 3}}])])
    return render_template("recipes.html",
                           page_title="All Recipes",
                           recipes=paginated_recipes,
                           recipe_paginated=paginated_recipes,
                           pagination=pagination,
                           products=products,
                           random_products=random_products)


# Recipe Page #
@app.route("/view_recipe/<recipe_id>", methods=["GET", "POST"])
def view_recipe(recipe_id):
    # Get one recipe from DB #
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    # 3 random products #
    products = mongo.db.products
    random_products = (
        [product for product in products.aggregate([
            {"$sample": {"size": 3}}])])
    return render_template("view_recipe.html", recipe=recipe,
                           products=products,
                           random_products=random_products,
                           page_title="Recipe")


# Search functionality #
@app.route("/search", methods=["GET", "POST"])
def search():
    # Search functionality #
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    # Pagination #
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination_obj = paginated(recipes, page)
    paginated_recipes = pagination_obj[0]
    pagination = pagination_obj[1]
    return render_template("recipes.html",
                           page_title="Search Result",
                           recipes=recipes,
                           total=len(recipes),
                           recipe_paginated=paginated_recipes,
                           pagination=pagination,
                           search=True)


# --- User Sites --- #
# User Profile Page #
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # 3 random products #
    products = mongo.db.products
    random_products = (
        [product for product in products.aggregate([
            {"$sample": {"size": 3}}])])
    # Retrieve users and recipes to use on profile page #
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    users = list(mongo.db.users.find())
    recipes = list(mongo.db.recipes.find())
    favourite_recipes = mongo.db.users.find_one(
                {"username": session["user"]})["favourite_recipes"]
    # Favourites Array #
    favourites = []
    # Push to Favourites Array #
    for recipe in favourite_recipes:
        favourites.append(mongo.db.recipes.find_one({"_id": recipe}))
    if session["user"]:
        if request.method == "POST":
            # finds the Users-Profile in db
            users = mongo.db.users.find_one(
                {"username": session["user"]})
            # Edit Password functionality #
            if str(request.form.get("password")) == str(
                    request.form.get("confirm-password")):
                newvalue = {"$set": {"password": generate_password_hash(
                    str(request.form.get("password")))}}
                mongo.db.users.update_one(users, newvalue)
                flash("Password successfully updated!", "success")
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                flash("Passwords don't match, try again!", "error")
        return render_template(
            "profile.html", username=username, users=users,
            recipes=recipes, favourites=favourites,
            random_products=random_products)

    return redirect(url_for("login"))


# Add Recipe Page #
# Add Object functionality to DB #
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    # Request form fields #
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "image": request.form.get("image"),
            "time": request.form.get("time"),
            "difficulty": request.form.get("difficulty"),
            "ingredients": request.form.get("ingredients"),
            "directions": request.form.get("directions"),
            "created_by": request.form.get("created_by"),
            "user": session["user"]
        }
        # add request to recipes DB #
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added", "success")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("add_recipe.html",
                           page_title="Add Recipe")


# Edit Recipe Page #
# Edit functionality linked with Profile Page #
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    # Request form fields #
    if request.method == "POST":
        recipe_edit = {
            "recipe_name": request.form.get("recipe_name"),
            "image": request.form.get("image"),
            "time": request.form.get("time"),
            "difficulty": request.form.get("difficulty"),
            "ingredients": request.form.get("ingredients"),
            "directions": request.form.get("directions"),
            "created_by": request.form.get("created_by"),
            "user": session["user"]
        }
        # update recipe on DB #
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, recipe_edit)
        flash("Recipe Successfully Updated", "success")
        return redirect(url_for("profile", username=session["user"]))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template(
        "edit_recipe.html", recipe=recipe, page_title="Edit Recipe")


# ON PROFILE PAGE #
# Delete recipe functionality #
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    list(mongo.db.users.find(
        {"favourite_recipes": ObjectId(recipe_id)}))
    # Remove recipe from array in DB #
    mongo.db.users.find_one_and_update(
            {"username": session["user"].lower()},
            {"$pull": {"favourite_recipes": ObjectId(recipe_id)}})
    flash("Recipe Deleted Successfully", "success")
    return render_template("profile.html")


# ON RECIPES AND VIEW_RECIPE PAGE #
# Add recipe funtionality to add recipes to Favourite List on Profile Page #
@app.route("/favourite_recipe/<recipe_id>", methods=["GET", "POST"])
def favourite_recipe(recipe_id):
    favourites = mongo.db.users.find(
        {"favourite_recipes": ObjectId(recipe_id)})
    recipe = mongo.db.users.find_one(
        {"favourite_recipes": ObjectId(recipe_id)})
    # Check favourite is not already added #
    if recipe in favourites:
        flash("This recipe is already in your favourites!", "error")
        return redirect(url_for("all_recipes"))

    # Add recipeId to favourites array in user collection #
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"].lower()},
            {"$push": {"favourite_recipes": ObjectId(recipe_id)}})
        flash("Recipe added to your favourites!", "success")
        return redirect(url_for("profile", username=session["user"]))


# Remove or delete recipe from favourites array in DB #
@app.route("/remove_recipe/<recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    favourites = list(mongo.db.users.find(
        {"favourite_recipes": ObjectId(recipe_id)}))
    mongo.db.users.find_one_and_update(
        {"username": session["user"].lower()},
        {"$pull": {"favourite_recipes": ObjectId(recipe_id)}})
    flash("Recipe removed from your favourites!", "success")
    return redirect(url_for(
        "profile", username=session["user"], favourites=favourites))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    products = mongo.db.products
    random_products = (
        [product for product in products.aggregate([
            {"$sample": {"size": 3}}])])
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "favourite_recipes": []
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!", "success")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("signup.html", page_title="Sign Up",
                           products=products,
                           random_products=random_products)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    products = mongo.db.products
    random_products = (
        [product for product in products.aggregate([
            {"$sample": {"size": 3}}])])
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password", "error")
                return redirect(url_for("signin"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password", "error")
            return redirect(url_for("signin"))

    return render_template("signin.html", page_title="Sign In",
                           products=products,
                           random_products=random_products)


@ app.route('/signout')
def signout():
    # remove user from session cookie
    flash("You have been logged out", "success")
    session.pop("user")
    return redirect(url_for('signin'))


# Subscribe Newsletter #
@ app.route('/sub', methods=['POST'])
def sub():
    if request.method == "POST":
        # check if username already exists in db
        existing_email = mongo.db.newsletter.find_one(
            {"email": request.form.get("email").lower()})

        if existing_email:
            flash("Email already exists", "error")
            return redirect(request.referrer)

        email = {
            "email": request.form.get("email").lower()
        }
        mongo.db.users.insert_one(email)

        sub = mongo.db.newsletter
        return_data = request.form.to_dict()
        sub.insert_one(return_data)
        flash("Sucessfully Subscribed", "success")
        return redirect(request.referrer)

    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
