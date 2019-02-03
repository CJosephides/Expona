"""
api.py
"""

import json
from uuid import uuid4
from bottle import Bottle, get, post, request, response, run
from expona.exponents import ExponentCalculator
from webrest.expona_db import ExponaDB
from utils.expona_logging import logger_factory
from utils.expona_time import epoch_now


db = ExponaDB()
api = Bottle()
WEBREST_SECRET = "DoIEvenWantThisJob?"
logger = logger_factory("api")


# User management
# ===============

@api.post("/user")
def create_user():

    data = request.json
    user = data["user"]
    password = data["pass"]
    result = db.create_user(user, password)
    if result:
        return "User {} successfully created.".format(user)
    else:
        return "Could not create user {}: already exists.".format(user)

@api.get("/user/<username>")
def login_user(username):

    try:
        data = request.json
        password = data["pass"]
    except (TypeError, KeyError):
        return "Must provide password through json; e.g. {'pass': *******}."

    print(username)
    print(password)

    if db.authenticate(username, password):
        response.set_cookie("user", username, secret=WEBREST_SECRET, path="/")
        return "User {user} logged in.".format(user=username)
    else:
        return "Failed to log in user {user}.".format(user=username)

def logged_in(username, request):

    cookie = request.get_cookie("user", secret=WEBREST_SECRET)
    return cookie == username

# Expona service
# ==============

@api.post("/user/<username>/expona")
def create_ExponentCalculator(username):

    if not logged_in(username, request):
        return "User {username} is not logged in.".format(username)

    timestamp = epoch_now()
    event_path = str(request.path)
    event_type = str(request.method)
    event_body = json.dumps(request.json)

    db.insert_log(username, timestamp, event_path, event_type, event_body)

@api.put("/expona")
def modify_ExponentCalculator():
    data = request.json

@api.get("/expona")
def calculate_exponents():

    data = request.json
    return {str(k): v for k, v in list(ec.expon([1,2,3]))}


if __name__ == "__main__":
    run(api, host="localhost", port=8080, debug=True)
