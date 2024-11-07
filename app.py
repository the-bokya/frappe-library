from flask import Flask, render_template
from .members.routes import route as members_route
from .books.routes import route as books_route
from .issue.routes import route as issue_route
from .transactions.routes import route as transactions_route
from .db import conn
from .helpers import datereader

app = Flask(__name__)
app.register_blueprint(members_route)
app.register_blueprint(books_route)
app.register_blueprint(issue_route)
app.register_blueprint(transactions_route)

# datereader converts string date to python date function
app.template_filter("datereader")(datereader)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")
