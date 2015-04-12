import hashlib
import base64
import os
import json
import sys

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug import secure_filename

app = Flask(__name__)

USER_DIR = "data/users"
PWD_SALT = b"secretsalt"

app.secret_key = "secretkey"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form.copy()
        data["password"] = hash_pwd(data["password"])
        file_path = (USER_DIR + "/{}.json".format(secure_filename(
            data["login"]))).encode(sys.getfilesystemencoding() or "utf-8")
        if not os.path.exists(file_path):
            with open(file_path, "wt") as file_:
                json.dump(data, file_)
            return redirect(url_for('index'))
        flash("Login já existente - tente novamente!")
    return render_template("register.html")


def hash_pwd(pwd):
    sha = hashlib.sha512(pwd.encode("utf-8") + PWD_SALT).digest()
    return base64.encodebytes(sha).decode("ascii")

if __name__ == "__main__":
    app.run(debug=True)
