from flask import Blueprint, render_template, request
from .models import read, create, delete, get_from_id, update

route = Blueprint("members", __name__, url_prefix="/members")


@route.route("/", methods=["GET"])
def view():
    members = read()
    return render_template("members/index.html", members=members, delete_mode=False)


@route.route("/create", methods=["GET", "POST"])
def create_view():
    if request.method == "GET":
        return render_template("members/create.html")
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


@route.route("/delete", methods=["GET", "POST"])
def delete_view():
    if request.method == "GET":
        members = read()
        # Note that I used a lot of conditional rendering in the index file
        # instead of creating a new delete.html file.
        # This is messy but prevents a lot of duplication and is clean in the long run.
        return render_template("members/index.html", members=members, delete_mode=True)
    if request.method == "POST":
        ids = request.form.getlist("delete")
        if delete(ids):
            return render_template(
                "success.html", message=f"Successfully deleted {len(ids)} IDs!"
            )
            return render_template(
                "failure.html", message=f"There was a problem deleting the IDs!"
            )


@route.route("/update", methods=["GET", "POST"])
def update_view():
    if request.method == "GET":
        id = request.args.get("id", default=-1, type=int)
        if id == -1:
            return render_template(
                "failure.html", message=f"Please provide an ID to update!"
            )
        member = get_from_id(id)
        return render_template("members/update.html", member=member)
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        timestamp = request.form["timestamp"]
        if update(id, name, timestamp):
            return render_template(
                "success.html", message=f"Successfully updated ID {id}!"
            )
        else:
            return render_template(
                "failure.html", message=f"There was a problem updating the ID!"
            )
