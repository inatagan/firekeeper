import sqlite3


# SQL Queries
CREATE_KARMA_TABLE = """CREATE TABLE IF NOT EXISTS karma (
            id INTEGER NOT NULL PRIMARY KEY,
            from_user TEXT NOT NULL,
            to_user TEXT NOT NULL,
            submission_id TEXT,
            comment_id TEXT,
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
            comment_id,
            submission_title,
            platform,
            subreddit)
            VALUES (?, ?, ?, ?, ?, ?, ?);"""


SYNC_KARMA_PLAT = """INSERT INTO karma (
            from_user,
            to_user,
            platform,
            subreddit)
            VALUES (?, ?, ?, ?);"""


SYNC_KARMA = """INSERT INTO karma (
            from_user,
            to_user,
            subreddit)
            VALUES (?, ?, ?);"""


GET_USER_KARMA = "SELECT COUNT(to_user) FROM karma WHERE to_user = ?;"


GET_ALL_TIME_CHAMPIONS = """SELECT to_user, COUNT(to_user) FROM karma GROUP BY to_user ORDER BY COUNT(to_user) DESC LIMIT 10;"""


GET_WEEKLY_CHAMPIONS = "SELECT to_user, COUNT(to_user) FROM karma WHERE date BETWEEN datetime('now', '-6 days') AND datetime('now') GROUP BY to_user ORDER BY COUNT(to_user) DESC LIMIT 20;"


DELETE_ALL_KARMA = "DELETE FROM karma WHERE to_user = ?;"


# Functions
def connect():
    return sqlite3.connect('summonsign.db')


def create_tables(connection):
    with connection:
        connection.execute(CREATE_KARMA_TABLE)


def add_karma(connection, from_user, to_user, submission_id, comment_id, submission_title, platform, subreddit):
    with connection:
        connection.execute(INSERT_KARMA, (from_user, to_user, submission_id, comment_id, submission_title, platform, subreddit))


def sync_karma(connection, from_user, to_user, subreddit):
    with connection:
        connection.execute(SYNC_KARMA, (from_user, to_user, subreddit))


def sync_karma_plat(connection, from_user, to_user, platform, subreddit):
    with connection:
        connection.execute(SYNC_KARMA_PLAT, (from_user, to_user, platform, subreddit))


def get_user_karma(connection, username):
    with connection:
        return connection.execute(GET_USER_KARMA, (username,)).fetchone()[0]


def get_all_time_champions(connection):
    with connection:
        return connection.execute(GET_ALL_TIME_CHAMPIONS).fetchall()


def get_weekly_champions(connection):
    with connection:
        return connection.execute(GET_WEEKLY_CHAMPIONS).fetchall()


def delete_all(connection, username):
    with connection:
        connection.execute(DELETE_ALL_KARMA, (username,))

