from flask import Blueprint, render_template, request
from .models import read, create, delete, get_from_id, update
from .import_books import import_books

route = Blueprint("books", __name__, url_prefix="/books")


@route.route("/", methods=["GET"])
def view():
    books = read()
    return render_template("books/index.html", books=books, delete_mode=False)


@route.route("/create", methods=["GET", "POST"])
def create_view():
    if request.method == "GET":
        book = dict()
        book["bookID"] = request.args.get("bookID", default=0, type=int)
        book["title"] = request.args.get("title", default="", type=str)
        book["authors"] = request.args.get("authors", default="", type=str)
        book["isbn"] = request.args.get("isbn", default="", type=str)
        book["language_code"] = request.args.get("language_code", default="", type=str)
        book["publication_date"] = request.args.get(
            "publication_date", default="", type=str
        )
        book["publisher"] = request.args.get("publisher", default="", type=str)
        book["amount"] = request.args.get("amount", default=0, type=int)

        return render_template("books/create.html", book=book)

    if request.method == "POST":
        bookID = request.form["bookID"]
        title = request.form["title"]
        authors = request.form["authors"]
        isbn = request.form["isbn"]
        language_code = request.form["language_code"]
        publication_date = request.form["publication_date"]
        publisher = request.form["publisher"]
        amount = request.form["amount"]
        if int(amount) <= 0:
            return render_template(
                "failure.html",
                message=f"Please enter a positive amount!",
            )
        if create(
            bookID=bookID,
            title=title,
            authors=authors,
            isbn=isbn,
            language_code=language_code,
            publication_date=publication_date,
            publisher=publisher,
            amount=amount,
        ):
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
        bookIDs = request.form.getlist("delete")
        if delete(bookIDs):
            return render_template(
                "success.html", message=f"Successfully deleted {len(bookIDs)} IDs!"
            )
        else:
            return render_template(
                "failure.html", message=f"There was a problem deleting the IDs!"
            )


@route.route("/update", methods=["GET", "POST"])
def update_view():
    if request.method == "GET":
        bookID = request.args.get("bookID", default=-1, type=int)
        if bookID == -1:
            return render_template(
                "failure.html", message=f"Please provide an ID to update!"
            )
        book = get_from_id(bookID)
        return render_template("books/update.html", book=book)
    if request.method == "POST":
        bookID = request.form["bookID"]
        title = request.form["title"]
        authors = request.form["authors"]
        isbn = request.form["isbn"]
        language_code = request.form["language_code"]
        publication_date = request.form["publication_date"]
        publisher = request.form["publisher"]
        amount = request.form["amount"]

        if update(
            bookID, title, authors, isbn, language_code, publication_date, publisher, amount
        ):
            return render_template(
                "success.html", message=f"Successfully updated ID {bookID}!"
            )
        else:
            return render_template(
                "failure.html", message=f"There was a problem updating the ID!"
            )


@route.route("/import", methods=["GET", "POST"])
def import_view():
    if request.method == "GET":
        return render_template("books/import.html", show_books=False)

    if request.method == "POST":
        bookID = request.form["bookID"]
        title = request.form["title"]
        authors = request.form["authors"]
        isbn = request.form["isbn"]
        language_code = request.form["language_code"]
        publication_date = request.form["publication_date"]
        publisher = request.form["publisher"]
        amount = request.form["amount"]

        if update(
            bookID=bookID,
            title=title,
            authors=authors,
            isbn=isbn,
            language_code=language_code,
            publication_date=publication_date,
            publisher=publisher,
            amount=amount,
        ):
            return render_template(
                "success.html", message=f"Successfully updated ID {bookID}!"
            )
        else:
            return render_template(
                "failure.html", message=f"There was a problem updating the ID!"
            )


@route.route("/import/search", methods=["GET"])
def search_view():
    if request.method == "GET":
        params = dict()
        title = request.args.get("title", default="", type=str)
        authors = request.args.get("authors", default="", type=str)
        isbn = request.args.get("isbn", default="", type=str)
        publisher = request.args.get("publisher", default="", type=str)

        books = import_books(
            title=title, authors=authors, isbn=isbn, publisher=publisher
        )
        print(books)
        return render_template("books/import.html", books=books, show_books=True)
