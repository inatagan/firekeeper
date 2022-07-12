import sys
from database import db_init as db
from sqlite3 import IntegrityError
# import flairsync


# This script must receive 4 arguments (username, karma, platform, subreddit)
# This is a work in progress, it is not complete and not to be used yet!!
def main():
    try:
        username = sys.argv[1]
    except IndexError:
        print("Error: Missing Arguments!")
    try:
        connection = db.connect()
        db.delete_all(connection, username)
        db_karma = db.get_user_karma(connection, username)
        print(f"user deleted from DB: {username} : {db_karma}")
        # flairsync.main(username)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()

