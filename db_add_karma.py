import sys
from database import db_init as db
from sqlite3 import IntegrityError
import flairsync


# This script must receive 4 arguments (username, karma, platform, subreddit)
def main():
    try:
        username = sys.argv[1]
        karma = int(sys.argv[2])
        plat = sys.argv[3]
        option = int(sys.argv[4])
        sub = 'SummonSign' if option < 1 else 'BeyondTheFog'
    except IndexError:
        print("Error: Missing Arguments!")
    try:
        connection = db.connect()
        db.create_tables(connection)
        for i in range(karma):
            try:
                db.sync_karma_plat(connection, '-Firekeeper-', username, plat, sub)
            except IntegrityError as err:
                print(err)
            except Exception as err:
                print(err)
        db_karma = db.get_user_karma(connection, username)
        print(f"userflair synced: {username} : {db_karma}")
        flairsync.main(username)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()

