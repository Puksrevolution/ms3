git push origin master


##### Create a MongoDB Database App
  - 



1. pip3 install Flask
2. touch .gitignore
```
env.py
__pycache__/
```
3. touch env.py (setting up default environment variable)
  - [RandomKeygen - The Secure Password & Keygen Generator](https://randomkeygen.com/)
    - Fort Knox Passwords - Secure enough for almost anything, like root or administrator passwords.
    - os.environ.setdefault("SECRET_KEY", "fort_knox_password_here")
  - MongoDB
    - Overwiev
    - connect
    - Connect your Application
    mongodb+srv://Puk:<password>@myfirstcluster.82ax2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
    mongodb+srv://Puk:Pa55w0rd@myfirstcluster.82ax2.mongodb.net/cook_book?retryWrites=true&w=majority
```
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "sXMca2*~NeVkEwz919@8*4ikHRvO^")
os.environ.setdefault("MONGO_URI", "mongodb+srv://Puk:Pa55w0rd@myfirstcluster.82ax2.mongodb.net/cook_book?retryWrites=true&w=majority")
os.environ.setdefault("MONGO_DBNAME", "cook_book")

```
4. touch app.py
```
import os
from flask import Flask
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
```
5. python3 app.py

- git add .
- git commit -m "Create the Flask App"
- git status (making sure env.py gets ignored)
- git push

6. pip3 freeze --local > requirements.txt
7. echo web: python app.py > Procfile
8. Heroku
  - create new app
  - app name
  - country Europe
  - create app
  - GitHub
    - repo name: ms3
    - search
    - connect
    - settings
    - Config Vars -> Reveal Config Vars
    - Key: IP, Value: 0.0.0.0
    - Key: PORT, Value: 5000
    - Key: SECRET_KEY, Value: sXMca2*~NeVkEwz919@8*4ikHRvO^
    - Key: MONGO_URI, Value: 
    mongodb+srv://Puk:Pa55w0rd@myfirstcluster.82ax2.mongodb.net/cook_book?retryWrites=true&w=majority
    - Key: MONGO_DBNAME, Value: cook_book

- git status
- git add requirements.txt
- git commit -m "Add requirements.txt"
- git add Procfile
- git commit -m "Add Procfile"
- git push

    - Deploy    
    - Enable Automatic Deploys
    - Deploy Branch


9. pip3 install flask-pymongo
10. pip3 install dnspython

- pip3 freeze --local > requirements.txt (after every pip3 install needed)

12. app.py
```
import os
from flask import (
    Flask, render_template, flash,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/add_recipe")
def add_recipe():
    recipe = mongo.db.favorites.find()
    return render_template("favorites.html", recipe=recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

```

- install Pagination
  - pip install -U flask-paginate


##### Search function

In Terminal
- python3   enter
- from app import mongo    enter
- mongo.db.recipes.create_index([("recipe_name", "text"), ("time", "text"), ("difficulty", "text"), ("ingredients", "text"), ("directions", "text"), ("created_by", "text") ])
- mongo.db.recipes.index_information()
- quit()

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