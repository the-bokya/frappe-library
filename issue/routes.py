from flask import Blueprint, render_template, request
from ..members.models import read as get_members, get_from_id as get_member_from_id
from ..books.models import read as get_books
from .models import issue

route = Blueprint("issue", __name__, url_prefix="/issue")


@route.route("/", methods=["GET", "POST"])
def issue_view():
    if request.method == "GET":
        memberid = request.args.get("memberid")
        member = get_member_from_id(memberid)
        books = get_books()
        if member["due_amount"] >= 500:
            return render_template(
                "failure.html",
                message=f"This user has too many books! Ask them to return a few first.",
            )
        return render_template("books/index.html", issue_mode=True, books=books, memberid=memberid)
    if request.method == "POST":
        bookid = request.form["bookid"]
        memberid = request.form["memberid"]
        if issue(bookid, memberid):
            return render_template(
                "success.html",
                message=f"Successfully rented away the book!",
            )
        else:
            return render_template(
                "failure.html",
                message=f"There was a problem renting the book. Please check again.",
            )
