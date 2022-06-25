from dotenv import load_dotenv
import os
import praw
from utils import karma
from database import db_init as db
import sqlite3


#Load user secret
load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ.get('my_client_id'),
    client_secret=os.environ.get('my_client_secret'),
    user_agent=os.environ.get('my_user_agent'),
    username=os.environ.get('my_username'),
    password=os.environ.get('my_password'),
)


def main():
    subreddit = reddit.subreddit("SummonSign")
    connection = db.connect()
    db.create_tables(connection)
    try:
        for flair in subreddit.flair():
            user_info = []
            user_info.append(flair['user'])
            user_info.append(flair['flair_text'])
            user_karma = karma.getKarmaCount(user_info)
            if user_karma > 1:
                db_karma_count = db.get_user_karma(connection, flair['user'].name)[0]
                print(f'{user_info[0]}, {user_karma} DB = {db_karma_count}')
                # print(flair)
                # user_css = karma.getCSSClass(user_karma)
                # syncFlair(subreddit, user_info, user_css)
                for i in range(user_karma):
                    try:
                        db.sync_karma(connection, '-Firekeeper-', flair['user'].name, 'SummonSign')
                    except sqlite3.IntegrityError as err:
                        print(err)
    except Exception as e:
        print(e)
    else:
        print('OMG IT WORKED!!\n\n ! ! SYNCED ! !')


if __name__ == '__main__':
    main()

