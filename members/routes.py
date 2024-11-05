from flask import Blueprint, render_template
from .models import read

route = Blueprint("members", __name__, url_prefix="/members")


@route.route("/", methods=["GET"])
def view():
    members = read()
    return render_template("members/index.html", members=members)
