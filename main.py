from flask import Flask,redirect,url_for,session, request, render_template
import settings
from functools import wraps
from db import *

app = Flask(__name__, template_folder=settings.TEMPLATES_URL, static_folder=settings.STATIC_URL)

def check(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'AUTH' not in session:
            return redirect("/auth")
        return func(*args, **kwargs)
    return inner

@app.route("/")
@app.route("/index")
@check
def index():
    user = getUser(session["user_login"])
    return render_template("about.html", user = user)


@app.route("/post/category/<category_name>", methods = ['POST','GET'])
@check
def post_category(category_name):
    category_id = getIdByCategory(category_name)
    errors = []
    if request.method == "POST":
        if not request.form["title"]:
            errors.append("Пустий загаловок")
        
        if not request.form["post"]:
            errors.append("Пустий текст")
        
        filename = None
        if request.files["image"].filename:
            img = request.files["image"]
            img.save(f"{settings.STATIC_URL}/{img.filename}")
            filename = img.filename

        if len(errors) == 0:
            addPost(category_id, request.form["post"],request.form["title"], filename)

    posts = getPostsByCategory(category_id)

    return render_template("post_category.html", posts=posts, name_category=category_name, category_id = category_id, errors = errors)


@app.route("/post/delete/<post_id>/<category_name>", methods = ['POST'])
@check
def post_delete(post_id, category_name):
    delPost(post_id)
    return redirect(f"/post/category/{category_name}")

@app.route("/auth", methods=['POST', 'GET'] )
def auth():
    errors = []
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]


        user = getUser(login)

        if not login:
            errors.append("не вказаний логін")

        if not user:
            errors.append("погані дані")

        elif not password:
            errors.append("не вказаний пароль")
        elif password != user["password"]:
            errors.append("не коректнний пароль")
  
        if len(errors) == 0:
            session["AUTH"] = True
            session["user_login"] = login
            return redirect('/')

    return render_template("auth.html", errors = errors)

@app.route("/out")
def out():
    session.clear()
    return redirect("/auth")

app.config["SECRET_KEY"] = "GGG"

if __name__ == '__main__':
    app.run(debug=True)
