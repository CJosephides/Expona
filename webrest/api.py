"""
api.py
"""

import json
from uuid import uuid4
from bottle import Bottle, get, post, request, run
from expona.exponents import ExponentCalculator
from utils.expona_logging import logger_factory

logger = logger_factory("api")
api = Bottle()

@api.post("/expona")
def create_ExponentCalculator():
    data = request.json
    logger.info("POST data: %s", data)

@api.put("/expona")
def modify_ExponentCalculator():
    data = request.json
    logger.info("PUT data: %s", data)

@api.get("/expona")
def calculate_exponents():

    data = request.json
    logger.info("GET data: %s", data)

    return {str(k): v for k, v in list(ec.expon([1,2,3]))}


#run(api, host="localhost", port=8080, debug=True)
