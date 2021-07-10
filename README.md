### Install Flask

1. pip3 install Flask
2. pip3 freeze --local > requirements.txt
3. touch .gitignore
  - .gitignore
```
env.py
__pycache__/
```
4. touch env.py
  - env.py
```
import os

os.environ.setdefault("SECRET_KEY", "your_secret_key_here")
```
5. echo web: python app.py > Procfile

6. touch app.py
  - app.py
```
import os
import json
from flask import Flask, render_template, request, flash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
```
### HTML/CSS/Basic

Folder
- templates
  - base.html
  - index.html
- static


```
import os
import json
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", page_title="Recipes")


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


@app.route("/result_favorites")
def resultFavorites():
    return render_template("result_favorites.html", page_title="My Favorite")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True) # debug changing to False when you are finishd with project
```



### Install Heroku

1. creat on Heroku a new app
  - name
  - country Europ

2. npm install -g heroku
3. heroku login -i
4. heroku apps

5. on Heroku
  - open app

6. git remote -v

7. on Heroku
  - settings
    - Config Vars -> Reveal Config Vars
    - Key: IP, Value: 0.0.0.0
    - Key: PORT, Value: 5000
    - Key: SECRET_KEY, Value: your_secret_key_here    
  - get Heroku git URL
https://git.heroku.com/cbms3.git
8. git remote add heroku https://git.heroku.com/cbms3.git
9. git push -u heroku master
10. git remote rm heroku
11. git remote -v

- git add .
- git commit -m ""
- git push origin master

11. on Heroku
  - Deploy
    - GitHub
    - repo name: ms3
    - search
    - connect
    - Enable Automatic Deploys
    - Deploy Branch





### HTML/CSS/Basic

```
import os
import json
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", page_title="Recipes")


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


@app.route("/result_favorites")
def resultFavorites():
    return render_template("result_favorites.html", page_title="My Favorite")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True) # debug changing to False when you are finishd with project
```


Credits
====

## Code

### [webstoked](https://webstoked.com/auto-update-copyright-year-javascript/)

```
Copyright © <span id="copyright-year">2020</span>

<script>
    document.querySelector('#copyright-year').innerText = new Date().getFullYear();
</script>
```

### [Bootstrap](https://getbootstrap.com/)

#### [Pagination](https://getbootstrap.com/docs/5.0/components/pagination/)
```
<nav class="mt-5" aria-label="Page navigation">
    <ul class="pagination justify-content-center">
        <li class="page-item disabled">
            <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item">
            <a class="page-link" href="#">Next</a>
        </li>
    </ul>
</nav>
```
#### [Album](https://getbootstrap.com/docs/5.0/examples/album/)
```
<div class="album">
    <div class="container">
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
            <div class="col mb-3">
                <div class="card">
                    <img src="{{ recipe.images }}"
                        class="img-fluid rounded" alt="...">
                    <div class="card-body">
                        <div class="card__content">
                            <h3> recipe.title </h3>
                            <p> recipe.rating </p>
                            <p>
                                <small class="text-muted">
                                    <i class="fas fa-hourglass-half"></i> : recipe.time
                                    <i class="fas fa-signal"></i> : recipe.severity
                                </small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col mb-3">
                <div class="card">
                    <img src="{{ url_for('static', filename='images/kaesekuchen-mit-2-schichten.jpg')}}"
                        class="img-fluid rounded" alt="...">
                    <div class="card-body">
                        <div class="card__content">
                            <h3> recipe.title </h3>
                            <p> recipe.rating </p>
                            <p>
                                <small class="text-muted">
                                    <i class="fas fa-hourglass-half"></i> : recipe.time
                                    <i class="fas fa-signal"></i> : recipe.severity
                                </small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col mb-3">
                <div class="card">
                    <img src="{{ url_for('static', filename='images/kaesekuchen-mit-2-schichten.jpg')}}"
                        class="img-fluid rounded" alt="...">
                    <div class="card-body">
                        <div class="card__content">
                            <h3> recipe.title </h3>
                            <p> recipe.rating </p>
                            <p>
                                <small class="text-muted">
                                    <i class="fas fa-hourglass-half"></i> : recipe.time
                                    <i class="fas fa-signal"></i> : recipe.severity
                                </small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col mb-3">
                <div class="card">
                    <img src="{{ url_for('static', filename='images/kaesekuchen-mit-2-schichten.jpg')}}"
                        class="img-fluid rounded" alt="...">
                    <div class="card-body">
                        <div class="card__content">
                            <h3> recipe.title </h3>
                            <p> recipe.rating </p>
                            <p>
                                <small class="text-muted">
                                    <i class="fas fa-hourglass-half"></i> : recipe.time
                                    <i class="fas fa-signal"></i> : recipe.severity
                                </small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col mb-3">
                <div class="card">
                    <img src="{{ url_for('static', filename='images/kaesekuchen-mit-2-schichten.jpg')}}"
                        class="img-fluid rounded" alt="...">
                    <div class="card-body">
                        <div class="card__content">
                            <h3> recipe.title </h3>
                            <p> recipe.rating </p>
                            <p>
                                <small class="text-muted">
                                    <i class="fas fa-hourglass-half"></i> : recipe.time
                                    <i class="fas fa-signal"></i> : recipe.severity
                                </small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col mb-3">
                <div class="card">
                    <img src="{{ url_for('static', filename='images/kaesekuchen-mit-2-schichten.jpg')}}"
                        class="img-fluid rounded" alt="...">
                    <div class="card-body">
                        <div class="card__content">
                            <h3> recipe.title </h3>
                            <p> recipe.rating </p>
                            <p>
                                <small class="text-muted">
                                    <i class="fas fa-hourglass-half"></i> : recipe.time
                                    <i class="fas fa-signal"></i> : recipe.severity
                                </small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>            
        </div>
    </div>
</div>
```



## Content

[Simly Recipes](https://www.simplyrecipes.com/)
- About Us
- Contact Us
- Terms of Use

[Anthony O' Brien](https://github.com/auxfuse)
- Privacy Policy
- Accessibility