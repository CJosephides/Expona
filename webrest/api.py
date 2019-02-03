"""
api.py
"""

from uuid import uuid4
from bottle import Bottle, get, post, request, run
from utils.expona_logging import logger_factory

logger = logger_factory("api")


api = Bottle()
