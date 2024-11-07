from flask import Blueprint, render_template, request
from .models import read, create, delete, get_from_id, update

route = Blueprint("books", __name__, url_prefix="/books")


@route.route("/", methods=["GET"])
def view():
    books = read()
    return render_template("books/index.html", books=books, delete_mode=False)


@route.route("/create", methods=["GET", "POST"])
def create_view():
    if request.method == "GET":
        return render_template("books/create.html")
    if request.method == "POST":
        id = request.form["bookID"]
        title = request.form["title"]
        authors = request.form["authors"]
        isbn = request.form["isbn"]
        language_code = request.form["language_code"]
        publication_date = request.form["publication_date"]
        publisher = request.form["publisher"]
        amount = request.form["amount"]
        if create(id, title, authors, isbn, language_code, publication_date, publisher, amount):
            return render_template(
                "success.html", message=f"Successfully created book {title}!"
            )
        return render_template(
            "failure.html",
            message=f"There was a problem creating the book {title}!",
        )


@route.route("/delete", methods=["GET", "POST"])
def delete_view():
    if request.method == "GET":
        books = read()
        # Note that I used a lot of conditional rendering in the index file
        # instead of creating a new delete.html file.
        # This is messy but prevents a lot of duplication and is clean in the long run.
        return render_template("books/index.html", books=books, delete_mode=True)
    if request.method == "POST":
        ids = request.form.getlist("delete")
        if delete(ids):
            return render_template(
                "success.html", message=f"Successfully deleted {len(ids)} IDs!"
            )
        else:
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
        book = get_from_id(id)
        return render_template("books/update.html", book=book)
    if request.method == "POST":
        id = request.form["bookID"]
        title = request.form["title"]
        authors = request.form["authors"]
        isbn = request.form["isbn"]
        language_code = request.form["language_code"]
        publication_date = request.form["publication_date"]
        publisher = request.form["publisher"]
        amount = request.form["amount"]

        if update(id, title, authors, isbn, language_code, publication_date, publisher, amount):
            return render_template(
                "success.html", message=f"Successfully updated ID {id}!"
            )
        else:
            return render_template(
                "failure.html", message=f"There was a problem updating the ID!"
            )