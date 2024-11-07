from flask import Blueprint, render_template, request
from ..members.models import read as get_members, get_from_id as get_member_from_id
from ..books.models import read as get_books
from .models import issue

route = Blueprint("issue", __name__, url_prefix="/issue")


@route.route("/", methods=["GET", "POST"])
def issue_view():
    if request.method == "GET":
        memberID = request.args.get("memberID")
        member = get_member_from_id(memberID)
        books = get_books()
        if member["due_amount"] >= 500:
            return render_template(
                "failure.html",
                message=f"This user has too many books! Ask them to return a few first.",
            )
        return render_template("books/index.html", issue_mode=True, books=books, memberID=memberID)
    if request.method == "POST":
        bookID = request.form["bookID"]
        memberID = request.form["memberID"]
        if issue(bookID, memberID):
            return render_template(
                "success.html",
                message=f"Successfully rented away the book!",
            )
        else:
            return render_template(
                "failure.html",
                message=f"There was a problem renting the book. Please check again.",
            )
