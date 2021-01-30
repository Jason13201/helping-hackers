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
        # String containing the problem submission
        # Store in db

        return render_template("submit.html")

    return render_template("home.html")


@app.route("/list")
def problemlist():
    # Retrieve all records from db
    pass