"""
    Code adapted from Code Institute Course Material
    Task Manager Flask App mini Project
"""


import os
from flask_paginate import Pagination, get_page_parameter
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Admin
ADMIN_USER_NAME = "admin"

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


# 3 random products
def get_random_products():
    products = list(mongo.db.products.aggregate([
            {"$sample": {"size": 3}}]))
    return products


"""
Render the Home, Article and
all the Footer pages
"""


@app.route("/")
def index():
    # 6 random recipes
    recipes = list(mongo.db.recipes.aggregate([
            {"$sample": {"size": 6}}]))
    # 3 random products
    products = get_random_products()
    return render_template("index.html",
                           page_title="Yummy Recipes",
                           recipes=recipes,
                           products=products)


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


"""
User account management
"""


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # 3 random products
    products = get_random_products()
    """
    Allows the user to create a new account with
    a unique username and password
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists", "error")
            return redirect(url_for("signup"))

        # collect the signup form data and write to MongoDB
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
                           products=products)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    # 3 random products
    products = get_random_products()
    """
    Allows the user to sign in with username and password.
    Checks for validity of username and password entered.
    Redirects user to profile page after successful login.
    """
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                # Welcome message and direct to Profile page
                flash("Welome Back!", "success")
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password", "error")
                return redirect(url_for("signin"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password", "error")
            return redirect(url_for("signin"))

    return render_template("signin.html", page_title="Sign In",
                           products=products)


@ app.route('/signout')
def signout():
    """
    Allows the user to logout and clear the session cookie
    """
    flash("You have been logged out", "success")
    session.pop("user")
    return redirect(url_for('index'))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    # 3 random products
    products = get_random_products()
    """
    Render the user profile page using the logged in user's
    data in the database.
    """
    # Retrieve users and recipes to use on profile page #
    username = session["user"]
    user_details = mongo.db.users.find_one({"username": session["user"]})
    favourite_recipe_id_list = user_details["favourite_recipes"]    
    recipes_by_me = []
    if username == ADMIN_USER_NAME:
        recipes_by_me = list(mongo.db.recipes.find())
    else:
        recipes_by_me = list(mongo.db.recipes.find({"user": username}))
    print(recipes_by_me)
    # Favourites Array #
    favourites = []
    # Push to Favourites Array #
    for recipe_id in favourite_recipe_id_list:
        is_valid_recipe = True
        try:
            recipe_detail = mongo.db.recipes.find_one({"_id": recipe_id})
            if not recipe_detail:
                is_valid_recipe = False
        except:
            is_valid_recipe = False
        if is_valid_recipe:
            favourites.append(recipe_detail)
    return render_template("profile.html",
                           username=username,
                           recipes_by_me=recipes_by_me,
                           favourites=favourites,
                           products=products)


@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        current_user = mongo.db.users.find_one(
            {"username": session["user"]})
        if str(request.form.get("password")) == str(
                request.form.get("confirm-password")):
            newvalue = {"$set": {"password": generate_password_hash(
                str(request.form.get("password")))}}
            mongo.db.users.update_one(current_user, newvalue)
            flash("Password successfully updated!", "success")
            return redirect(url_for("profile", username=session["user"]))
        else:
            flash("Passwords don't match, try again!", "error")
            return redirect(url_for("profile", username=session["user"]))
    return redirect(url_for("profile", username=session["user"]))


"""
Recipe CRUD Functionality
"""


@app.route("/all_recipes")
def all_recipes():
    """
    Render the Recipes page for all site visitors
    """
    # Get all recipes from DB #
    recipes = list(mongo.db.recipes.find().sort("_id", -1))
    # Pagination #
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination_obj = paginated(recipes, page)
    paginated_recipes = pagination_obj[0]
    pagination = pagination_obj[1]
    # 3 random products
    products = get_random_products()

    return render_template("recipes.html",
                           page_title="All Recipes",
                           recipes=paginated_recipes,
                           recipe_paginated=paginated_recipes,
                           pagination=pagination,
                           products=products)


@app.route("/view_recipe/<recipe_id>", methods=["GET", "POST"])
def view_recipe(recipe_id):
    """
    Get the recipe details for the selected recipe and
    render the View Recipe Page
    """
    # Get one recipe from DB #
    recipe = None
    try:
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    except:
        abort(404)

    # 3 random products #
    products = get_random_products()

    return render_template("view_recipe.html", recipe=recipe,
                           products=products,
                           page_title="Recipe")


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Render the Add Recipe page if a user is logged in.
    """
    # collect the add recipe form data and write to MongoD
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "image": request.form.get("image"),
            "time": request.form.get("time"),
            "difficulty": request.form.get("difficulty"),
            "ingredients": request.form.get("ingredients"),
            "directions": request.form.get("directions"),
            "created_by": session["user"],
            "user": session["user"]
        }
        # add collect data to recipes DB #
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added", "success")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("add_recipe.html",                           
                           page_title="Add Recipe")


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Render the Edit Recipe page if a user is logged in.
    """
    if not session["user"]:
        return redirect(url_for("index"))

    # Request form fields #
    if request.method == "POST":
        # grab the session user's details from db
        username = session["user"]
        # grab the recipe details
        recipe = mongo.db.recipes.find_one(
            {"_id": ObjectId(recipe_id)})
        print(recipe)

        # if it's user or admin then allow edit
        if session["user"] == recipe["user"] or username == ADMIN_USER_NAME:

            recipe_edit = {
                "recipe_name": request.form.get("recipe_name"),
                "image": request.form.get("image"),
                "time": request.form.get("time"),
                "difficulty": request.form.get("difficulty"),
                "ingredients": request.form.get("ingredients"),
                "directions": request.form.get("directions"),
                "created_by": request.form.get("created_by"),
                "user": username
            }
            # update recipe on DB #
            mongo.db.recipes.update_one(
                {"_id": ObjectId(recipe_id)},
                {"$set": recipe_edit})
            flash("Recipe Successfully Updated", "success")
            return redirect(url_for("profile", username=session["user"]))

    recipe = None
    try:
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    except:
        abort(404)
    return render_template("edit_recipe.html",
                           recipe=recipe, page_title="Edit Recipe")


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """
    Delete Recipe function
    deletes the selected Recipe from the database.
    """
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    # Remove recipe from array in DB #
    mongo.db.users.find_one_and_update(
            {"username": session["user"].lower()},
            {"$pull": {"favourite_recipes": ObjectId(recipe_id)}})
    flash("Recipe Successfully Deleted", "success")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Search function
    filters the recipes based on the text index query.
    """
    # Search functionality #
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    # Pagination #
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination_obj = paginated(recipes, page)
    paginated_recipes = pagination_obj[0]
    pagination = pagination_obj[1]
    # 3 random products
    products = get_random_products()

    return render_template("recipes.html",
                           page_title="Search Result",
                           query=query,
                           recipes=recipes,
                           total=len(recipes),
                           recipe_paginated=paginated_recipes,
                           pagination=pagination,
                           search=True,
                           products=products)


"""
Recipe add favourite button functionality
"""


@app.route("/favourite_recipe/<recipe_id>", methods=["GET", "POST"])
def favourite_recipe(recipe_id):
    """
    Allows the user to add a recipe to their personal
    favourites list
    """
    if session["user"]:
        favourite_recipe_ids = mongo.db.users.find_one(
            {"username": session["user"]})["favourite_recipes"]
        print(favourite_recipe_ids)
        print(recipe_id)

        # Check favourite is not already added #
        if ObjectId(recipe_id) in favourite_recipe_ids:
            flash("This recipe is already in your favourites!", "error")
            return redirect(url_for("all_recipes"))

        # Add recipeId to favourites array in user collection #
        else:
            mongo.db.users.find_one_and_update(
                {"username": session["user"].lower()},
                {"$push": {"favourite_recipes": ObjectId(recipe_id)}})
            flash("Recipe added to your favourites!", "success")
            return redirect(url_for("profile", username=session["user"]))


"""
Recipe remove favourite button functionality
"""


@app.route("/remove_favourite/<recipe_id>", methods=["GET", "POST"])
def remove_favourite(recipe_id):
    """
    Remove Recipe function
    removes the favourite Recipe from the database.
    """
    mongo.db.users.find_one_and_update(
        {"username": session["user"].lower()},
        {"$pull": {"favourite_recipes": ObjectId(recipe_id)}})
    flash("Recipe removed from your favourites!", "success")
    return redirect(url_for("profile", username=session["user"]))


"""
Subscribe Newsletter Functionality
collect the email address from input field and write to Mongo DB
"""


@app.route('/sub', methods=['POST'])
def sub():
    if request.method == "POST":
        # check if username already exists in db
        existing_email = mongo.db.newsletter.find_one(
            {"email": request.form.get("email").lower()})

        if existing_email:
            flash("Email already exists", "error")
            return redirect(request.referrer)

        sub = mongo.db.newsletter
        return_data = request.form.to_dict()
        sub.insert_one(return_data)
        flash("Successfully Subscribed", "success")
        return redirect(request.referrer)

    return redirect(request.referrer)


"""
HTTP response error code handling.
"""


@app.errorhandler(404)
def not_found(e):
    """
    Renders an error page for http error respons code 404
    displaying a friendly template with a button that directs the user
    back to the main page.
    """
    return (render_template('404.html'), 404)


@app.errorhandler(500)
def internal_server_error(e):
    """
    Renders an error page for http error respons code 500
    displaying a friendly template with a button that directs the user
    back to the main page.
    """
    return (render_template('500.html'), 500)


@app.errorhandler(503)
def service_unavailable(e):
    """
    Renders an error page for http error respons code 503
    displaying a friendly template with a button that directs the user
    back to the main page.
    """
    return (render_template('503.html'), 503)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
