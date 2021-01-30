import json
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


def getSolves(p_id):
    global problems

    for prob_id, _, solves in problems:
        if prob_id == p_id:
            return solves


@app.route("/list", methods=["GET", "POST"])
def problemlist():
    global problems

    if request.form:
        p_id, username, link = [
            request.form.get(name) for name in ["id", "username", "link"]
        ]
        p_id = int(p_id)
        currentSolves = getSolves(p_id)
        solves = [[username, link]] + (currentSolves if currentSolves else [])
        session.execute(
            "UPDATE breakfast.problems SET solves = %s WHERE id = %s",
            (json.dumps(solves), p_id),
        )

    # Retrieve all records from db
    problems = [
        (row.id, row.column, json.loads(row.solves) if row.solves else None)
        for row in session.execute("SELECT id, column, solves FROM breakfast.problems;")
    ]
    print(problems)
    return render_template("list.html", problems=problems)


@app.route("/deleteall")
def deleteall():
    global problemId
    problemId = 1
    session.execute("TRUNCATE breakfast.problems")
    return redirect(url_for("home"))