import sqlite3


conn = sqlite3.connect('summonsign.db')

cursor = conn.cursor()


cursor.execute("""CREATE TABLE karma (
    from text,
    to text,
    submission_id text,
    submission_title text,
    platform text
    subreddit text,
    date date,
)""")

