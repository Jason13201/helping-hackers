from flask import render_template, url_for, request
from hh import app


from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config import username, password

cloud_config = {"secure_connect_bundle": "secure-connect-breakfastproblems.zip"}
auth_provider = PlainTextAuthProvider(username, password)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

id = 1


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
        global id
        session.execute(
            """
        INSERT INTO breakfast.problems (id, column)
        VALUES (%s, %s)
        """,
            (id, problemDetails),
        )
        id += 1

        return render_template("submit.html")

    return render_template("home.html")


@app.route("/list")
def problemlist():
    # Retrieve all records from db
    listOfProblems = []
    rows = session.execute("SELECT id, column FROM breakfast.problems;")
    for row in rows:
        listOfProblems.append(row.column)
    pass