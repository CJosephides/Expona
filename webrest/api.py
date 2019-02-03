"""
api.py
"""

import re
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

EXPONA_RE = re.compile("\/user\/.*?\/expona")


# ExponentCalculator utilities
# ============================

class ExponaCache:
    """
    Cache of ExponentCalculators.
    """

    cache = {}

    @classmethod
    def add_calculator(cls, user, calculator, latest_time):
        cls.cache[user] = (calculator, latest_time)

    @classmethod
    def get_calculator(cls, user):
        if user in cls.cache:
            return cls.cache[user][0]
        else:
            return None

    @classmethod
    def cache_fresh(cls, user, latest_time):
        if user not in cls.cache:
            return False

        return cls.cache[user][1] >= latest_time

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


def reconstruct_exponents(logs):
    """
    Reconstruct ExponentCalculator state (exponents) from API logs.
    """

    exponents = []
    latest_time = 0

    for log in logs:

        if not EXPONA_RE.search(log.path):
            continue

        # Get data.
        data = json.loads(log.body)
        if data:
            try:
                new_exponents = data["exponents"]
            except KeyError:
                logger.warning("Invalid exponent body in event log: %r.", log)

        # Reset or expand exponents.
        if log.type == "POST":
            exponents = new_exponents
        elif log.type == "PUT":
            exponents += new_exponents

        if log.time > latest_time:
           latest_time = log.time

    return exponents, latest_time


@api.get("/user/<username>/expona")
def expon_ExponentCalculator(username):

    if not logged_in(username, request):
        return "User {username} is not logged in.".format(username)

    data = request.json
    if not data:
        return "Must provide numbers to exponentiate in json; e.g. {'numbers': [1, 2, 3]}"
    numbers = data.get("numbers", [])

    # Reconstruct ExponentCalculator state from logs.
    logs = db.retrieve_expona_logs(username, before=None, exclude_get=True)
    exponents, latest_time = reconstruct_exponents(logs)

    # Check if cached.
    if ExponaCache.cache_fresh(username, latest_time):
        # Cached and fresh.
        logger.debug("Calculator is fresh.")
        calculator = ExponaCache.get_calculator(username)
    else:
        # Does not exist or is stale.
        logger.debug("Calculator does not exist or is stale.")
        calculator = ExponentCalculator(exponents)
        ExponaCache.add_calculator(username, calculator, latest_time)

    results = list(calculator.expon(numbers))  # TODO streaming?!?!
    return json.dumps(results)


@api.put("/user/<username>/expona")
def modify_ExponentCalculator(username):

    if not logged_in(username, request):
        return "User {username} is not logged in.".format(username)

    timestamp = epoch_now()
    event_path = str(request.path)
    event_type = str(request.method)
    event_body = json.dumps(request.json)

    db.insert_log(username, timestamp, event_path, event_type, event_body)


if __name__ == "__main__":
    run(api, host="localhost", port=8080, debug=True)
