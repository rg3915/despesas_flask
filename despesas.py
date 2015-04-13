import hashlib
import base64
import os
import json
import sys

from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Por favor, faça o login"
login_manager.login_message_category = "info"

USER_DIR = "data/users"
PWD_SALT = b"secretsalt"

app.secret_key = "secretkey"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/person", methods=["GET", "POST"])
def person_add():
    form = persons.PersonForm()
    if form.validate_on_submit():
        p = persons.PersonModel(
            form.first_name.data, form.last_name.data or "", form.email.data, form.site.data or "", form.job.data or "")
        db.session.add(p)
        db.session.commit()
        flash("Dados gravados com sucesso.")
        return redirect(url_for("person_add"))
    return render_template("person_add.html", form=form)

    # TODO: INCOMPLETE


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form.copy()
        data["password"] = hash_pwd(data["password"])
        # file_path = (USER_DIR + "/{}.json".format(secure_filename(
        # data["login"]))).encode(sys.getfilesystemencoding() or "utf-8")
        file_path = make_user_filename(data["login"])
        if not os.path.exists(file_path):
            with open(file_path, "wt") as file_:
                json.dump(data, file_)
            return redirect(url_for('index'))
        flash("Login já existente - tente novamente!")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.form
        file_path = make_user_filename(data["login"])
        pwd = hash_pwd(data["password"])
        try:
            user_data = json.load(open(file_path))
            if user_data["password"] == pwd:
                user = User(**user_data)
                login_user(user)
                flash("Logado com sucesso!")
                return redirect(request.args.get("next") or url_for("index"))
        except IOError:
            pass
        flash("Usuário ou senha incorretos!")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você não está mais autenticado")
    return redirect(url_for("index"))


@login_manager.user_loader
def load_user(userid):
    file_name = make_user_filename(userid)
    try:
        data = json.load(open(file_name))
    except IOError:
        return None
    return User(**data)


def make_user_filename(userid):
    return (USER_DIR + "/{}.json".format(secure_filename(
        userid))).encode(sys.getfilesystemencoding() or "utf-8")


def hash_pwd(pwd):
    sha = hashlib.sha512(pwd.encode("utf-8") + PWD_SALT).digest()
    return base64.encodebytes(sha).decode("ascii")


class User(UserMixin):

    def __init__(self, **kw):
        self.id = kw.pop("login")
        self.nome = kw.pop("nome", "")
        super().__init__()


if __name__ == "__main__":
    app.run(debug=True)
