import sqlite3

def connect():
    return sqlite3.connect('test.db')


def create_table(connection):
    with connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS dupe (
            col1 TEXT,
            col2 TEXT,
            col3 TEXT,
            CONSTRAINT unq UNIQUE (col1, col2, col3)
            )""")



# def add(connection, a,b,c):
#     try:
#         with connection:
#             connection.execute('INSERT INTO dupe (col1, col2, col3) VALUES (?,?,?)', (a,b,c))
#     except sqlite3.IntegrityError as err:
#         return err


def add(connection, a,b,c):
    with connection:
        connection.execute('INSERT INTO dupe (col1, col2, col3) VALUES (?,?,?)', (a,b,c))



def select(connection):
    with connection:
        return connection.execute('SELECT * FROM dupe').fetchall()