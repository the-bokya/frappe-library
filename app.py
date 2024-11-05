from flask import Flask, render_template
from .members.routes import route as members_route
from .db import conn

app = Flask(__name__)
app.register_blueprint(members_route)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")
