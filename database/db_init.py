import sqlite3


# SQL Queries
CREATE_KARMA_TABLE = """CREATE TABLE IF NOT EXISTS karma (
            id INTEGER PRIMARY KEY,
            from_user TEXT NOT NULL,
            to_user TEXT NOT NULL,
            submission_id TEXT,
            submission_title TEXT,
            platform TEXT,
            subreddit TEXT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT unq UNIQUE (from_user, to_user, submission_id)
        );"""


INSERT_KARMA = """INSERT INTO karma (
            from_user,
            to_user,
            submission_id,
            submission_title,
            platform,
            subreddit)
            VALUES (?, ?, ?, ?, ?, ?);"""


SYNC_KARMA = """INSERT INTO karma (
            from_user,
            to_user,
            subreddit)
            VALUES (?, ?, ?);"""


GET_USER_KARMA = "SELECT COUNT(to_user) FROM karma WHERE to_user = ?;"


# Functions
def connect():
    return sqlite3.connect('summonsign.db')


def create_tables(connection):
    with connection:
        connection.execute(CREATE_KARMA_TABLE)


def add_karma(connection, from_user, to_user, submission_id, submission_title, platform, subreddit):
    with connection:
        connection.execute(INSERT_KARMA, (from_user, to_user, submission_id, submission_title, platform, subreddit))


def sync_karma(connection, from_user, to_user, subreddit):
    with connection:
        connection.execute(SYNC_KARMA, (from_user, to_user, subreddit))


def get_user_karma(connection, username):
    with connection:
        return connection.execute(GET_USER_KARMA, (username,)).fetchone()


def get_weekly_users(connection):
    pass


def get_all_time_users(connection):
    pass