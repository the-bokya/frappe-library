from flask import Blueprint, render_template, request
from .models import view_transactions, return_book

route = Blueprint("transactions", __name__, url_prefix="/transactions")


@route.route("/", methods=["GET"])
def view():
    transactions = view_transactions()
    return render_template("transactions/index.html", transactions=transactions)

@route.route("/return", methods=["POST"])
def return_book_view():
    transactionid = request.form["transactionid"]
    if return_book(transactionid):
        return render_template("success.html", message="Successfully returned the book!")
    else:
        return render_template("failure.html", message="There was a problem returning the book, please try again.")