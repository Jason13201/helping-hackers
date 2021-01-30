from flask import render_template, url_for, request, redirect
from hh import app


from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config import username, password

cloud_config = {"secure_connect_bundle": "secure-connect-breakfastproblems.zip"}
auth_provider = PlainTextAuthProvider(username, password)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

problems = session.execute("SELECT id FROM breakfast.problems;")

problemId = 1 + max([row.id for row in problems]) if problems else 1


@app.route("/", methods=["GET", "POST"])
def home():
    global problemId
    if (
        request.form
        and "problem-details" in request.form
        and request.form["problem-details"]
    ):
        problemDetails = request.form["problem-details"]
        print(problemDetails)
        session.execute(
            """
        INSERT INTO breakfast.problems (id, column)
        VALUES (%s, %s)
        """,
            (problemId, problemDetails),
        )
        problemId += 1

        return render_template("submit.html")

    return render_template("home.html")


@app.route("/list")
def problemlist():
    # Retrieve all records from db
    problems = [
        (row.id, row.column)
        for row in session.execute("SELECT id, column FROM breakfast.problems;")
    ]
    print(problems)
    return render_template("list.html", problems=problems)


@app.route("/deleteall")
def deleteall():
    session.execute("TRUNCATE breakfast.problems")
    return redirect(url_for("home"))