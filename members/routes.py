from flask import Blueprint, render_template, request
from .models import read, create

route = Blueprint("members", __name__, url_prefix="/members")


@route.route("/", methods=["GET"])
def view():
    members = read()
    return render_template("members/index.html", members=members)


@route.route("/create", methods=["GET", "POST"])
def create_view():
    if request.method == "GET":
        members = read()
        return render_template("members/create.html", members=members)
    if request.method == "POST":
        name = request.form["name"]
        if create(name):
            return render_template(
                "success.html", message=f"Successfully created member {name}!"
            )
        return render_template(
            "failure.html",
            message=f"There was a problem creating the member {name}!",
        )
