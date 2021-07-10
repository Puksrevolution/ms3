import os
# import json
from flask import Flask, render_template, request, flash, redirect, url_for, session


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", page_title="Yummy Recipes")


@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html", page_title="Accessibility")


@app.route("/terms")
def terms():
    return render_template("terms.html", page_title="Terms of Use & Policies")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", page_title="Privacy Policy")


@app.route("/about")
def about():
    return render_template("about.html", page_title="About Us")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact Us")


@app.route("/profile")
def profile():
    return render_template("profile.html", page_title="Profile")


@app.route("/add_recipe")
def addRecipe():
    return render_template("add_recipe.html", page_title="Add Recipe")


@app.route("/favorites")
def favorites():
    return render_template("favorites.html", page_title="My Favorites")


@app.route("/register")
def register():
    return render_template("register.html", page_title="Register")


@app.route("/login")
def login():
    return render_template("login.html", page_title="Log In")


@app.route("/result_recipe")
def resultRecipe():
    return render_template("result_recipe.html", page_title="Recipe")


@app.route("/result_recipes")
def resultRecipes():
    return render_template("result_recipes.html", page_title="Recipes")

@app.route("/result_favorites")
def resultFavorites():
    return render_template("result_favorites.html", page_title="My Favorite")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
