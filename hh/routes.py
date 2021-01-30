from flask import render_template, url_for, request
from hh import app


@app.route("/", methods=["GET", "POST"])
def home():
    if (
        request.form
        and "problem-details" in request.form
        and request.form["problem-details"]
    ):
        problemDetails = request.form["problem-details"]
        print(problemDetails)
    return render_template("home.html")


@app.route("/list")
def problemlist():
    pass