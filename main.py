from random import randint

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, login_user, logout_user

import repositories
from forms.SignInForm import SignInForm
from forms.SignUpForm import SignUpForm
from models import *
from utils import Link


def generate_users(n: int):
    for i in range(n):
        age = randint(1, 100)
        user = User(
            i,
            "test@example.com",
            "".join([chr(randint(73, 89)) for _ in range(randint(5, 15))]),
            age,
            f"city{i}",
            "12345"
        )
        repositories.add_user(user)


def addUser(email, name, age, city, password):
    user = User(None, email, name, age, city, password)
    repositories.add_user(user)


app = Flask(__name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return repositories.get_user(user_id)


@app.route('/')
@login_required
def index():
    users = repositories.get_users()
    return render_template(
        'layout/layout.html',
        links=[
            Link("Home", "/"),
            Link("Add User", "/add")
        ],
        users=users
    )


@app.route("/add", methods=['GET', 'POST'])
@login_required
def signUp():
    form = SignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        age = form.age.data
        city = form.city.data
        password = form.password.data
        confirm_password = form.consfirm_password.data

        if password != confirm_password:
            return render_template(
                "formTemplate.html",
                form=form,
                btn_name="Регистрация!",
                error="Пароли не совпадают!"
            )

        addUser(email, name, age, city, password)
        return redirect("/users")

    return render_template("formTemplate.html", form=form, btn_name="Регистрация!")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = SignInForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        users = repositories.get_users()
        for user in users:
            if user.email == email and user.password == password:
                login_user(user)
                return redirect("/")

        return redirect("/login")

    return render_template("formTemplate.html", form=form, btn_name="Регистрация!")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/users/<int:user_id>")
@login_required
def getUser(user_id: int):
    users = repositories.get_users()

    for user in users:
        if user.id == user_id:
            return render_template(
                "layout/user-layout.html",
                links=[
                    Link("Home", "/"),
                    Link("Add User", "/add"),
                    Link("Delete User", f"/delUser/{user.id}", class_name="bg-danger"),
                ],
                user=user
            )

    return redirect("/")


@app.route("/delUser/<int:user_id>")
@login_required
def delUser(user_id: int):
    users = repositories.get_users()

    for user in users:
        if user.id == user_id:
            repositories.delete_user(user)

    return redirect("/")


if __name__ == '__main__':
    login_manager.init_app(app)
    app.app_context().push()
    repositories.create_table()

    # generate_users(10)

    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(debug=True, port=8080)
