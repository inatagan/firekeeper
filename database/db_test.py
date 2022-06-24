import sqlite3

connection = sqlite3.connect('test.db')

with connection:
    connection.execute("""CREATE TABLE IF NOT EXISTS dupe (
        col1 TEXT,
        col2 TEXT,
        col3 TEXT,
        CONSTRAINT unq UNIQUE (col1, col2, col3)
        )""")


try:
    with connection:
        connection.execute('INSERT INTO dupe (col1, col2, col3) VALUES (?,?,?)', ('a','b', None))
except sqlite3.IntegrityError as err:
    print(err)

with connection:
    print(connection.execute('SELECT * FROM dupe').fetchall())