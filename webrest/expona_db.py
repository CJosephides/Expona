"""
expona_db.py
"""

from contextlib import contextmanager
from config import ROOT_DIR
from os import path
import sqlite3
from collections import namedtuple
from utils.expona_logging import logger_factory
from utils.expona_time import epoch_now


DB_NAME = path.join(ROOT_DIR, "data", "expona.db")
ExponaLog = namedtuple("ExponaLog", "path type time body")
logger = logger_factory("db")


class ExponaDB:
    """
    Database interface.
    """

    def __init__(self, db_name=DB_NAME, initialize=False):
        self.conn = sqlite3.connect(db_name)
        if initialize:
            self.initialize_db()

    def transaction(self):
        """Context manager for db transaction."""

        @contextmanager
        def db_transaction():
            cursor = self.conn.cursor()
            yield cursor
            self.conn.commit()
            cursor.close()

        return db_transaction()

    def initialize_db(self):
        """Create database tables."""

        logger.info("Initializing database.")

        with self.transaction() as t:
            # USER
            t.execute("CREATE TABLE user (user char(100) primary key, pass char(100))")
            # LOG
            t.execute("CREATE TABLE log (id integer primary key, user char(100), time real, path char(100), type char(10), body char(1000))")

    def authenticate(self, user, password):
        """Return True if user, password pair exists in database."""

        with self.transaction() as t:
            r = t.execute("SELECT count(*) FROM user WHERE user = ? AND pass = ?", (user, password)).fetchone()

        if r[0] == 1:
            return True
        else:
            return False

    def create_user(self, user, password):
        """
        Create user, with password, if it does not exist in the db already.

        Returns True on successful user creation; otherwise, False.
        """

        with self.transaction() as t:
            r = t.execute("SELECT count(*) FROM user WHERE user = ?", (user,)).fetchone()

        if r[0] == 1:
            return False
        else:
            with self.transaction() as t:
                r = t.execute("INSERT INTO user (user, pass) values (?, ?)", (user, password))
            return True

    def insert_log(self, user, timestamp, event_path, event_type, event_body):
        """
        Insert an event log.

        Note that timestamp must be in (integer) seconds since the unix epoch.

        Returns True on successful insert; otherwise, False.
        """

        with self.transaction() as t:
            t.execute("INSERT INTO log (user, time, path, type, body) values (?, ?, ?, ?, ?)",
                      (user, timestamp, event_path, event_type, event_body))

        return True

    def retrieve_expona_logs(self, user, before=None, exclude_get=True):
        """
        Retrieve all entries from the 'log' table for user that were recorded before some time point.

        Parameters
        ----------
        exclude_post: bool
                      If True, exclude /user/<username>/expona POST requests.
        """

        if not before:
            before = epoch_now()

        if exclude_get:
            where_clause = "type <> 'GET'"
        else:
            where_clause = "1 = 1"

        with self.transaction() as t:
            results = t.execute(
                    "SELECT path, type, time, body FROM log WHERE user = ? AND time <= ? AND {where}".format(
                     where=where_clause), (user, before)).fetchall()

        logs = []
        for r in results:
            logs.append(ExponaLog(path=r[0], type=r[1], time=r[2], body=r[3]))

        return logs
