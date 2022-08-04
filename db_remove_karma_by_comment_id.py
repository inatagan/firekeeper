import sys
from database import db_init as db
from sqlite3 import IntegrityError
import flairsync


# This script must receive 2 arguments (comment_id, username)
def main():
    try:
        username = sys.argv[1]
        comment_id = sys.argv[2]
    except IndexError:
        print("Error: Missing Arguments!")
    connection = db.connect()
    db_karma = db.get_user_karma(connection, username)
    print(f"user to remove karma: {username} : {db_karma}")
    try:
        db.delete_by_comment_id(connection, comment_id)
    except Exception as err:
        print(err)
    else:
        db_karma = db.get_user_karma(connection, username)
        print(f"user info updated: {username} : {db_karma}")
        flairsync.main(username)


if __name__ == '__main__':
    main()

