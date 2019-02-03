"""
expona_db.py
"""

from contextlib import contextmanager
from config import ROOT_DIR
from os import path
import sqlite3
from utils.expona_logging import logger_factory


DB_NAME = path.join(ROOT_DIR, "data", "expona.db")
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
            t.execute("CREATE TABLE log (id integer primary key, user char(100), time integer, path char(100), type char(10), body char(1000))")

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
