from random import randint

from flask import Flask, render_template, redirect

from forms.SignUpForm import SignUpForm
from models import *

users = []


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
        users.append(user)


def addUser(email, name, age, city, password):
    if len(users) == 0:
        last_id = 0
    else:
        last_id = max(users, key=lambda x: x.id).id + 1

    user = User(last_id, email, name, age, city, password)
    users.insert(0, user)


app = Flask(__name__)


@app.route("/signUp", methods=['GET', 'POST'])
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


@app.route("/users", methods=['GET', 'POST'])
def getUsers():
    return render_template("users/list.html", users=users, count=len(users))


@app.route("/users/<int:user_id>")
def getUser(user_id: int):
    for user in users:
        if user.id == user_id:
            return render_template("users/user.html", user=user)

    return redirect("/users")


@app.route("/delUser/<int:user_id>")
def delUser(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)

    return redirect("/users")


if __name__ == '__main__':
    generate_users(10)
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(debug=True)
