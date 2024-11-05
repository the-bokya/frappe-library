from flask import Flask, render_template
from db import conn

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")
