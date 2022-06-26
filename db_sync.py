from dotenv import load_dotenv
import os
import praw
from utils import karma
from database import db_init as db
from sqlite3 import IntegrityError
from progress.bar import Bar



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
        for flair in Bar('Processing').iter(subreddit.flair()):
            if not karma.user_is_valid(reddit, subreddit, flair['user'].name):
                print(f"userflair deleted: {flair['user'].name}")
                subreddit.flair.delete(redditor=flair['user'].name)
            else:

                user_info = []
                user_info.append(flair['user'])
                user_info.append(flair['flair_text'])
                user_karma = karma.getKarmaCount(user_info)


                if user_karma > 1:
                    db_karma_count = db.get_user_karma(connection, flair['user'].name)
                    if user_karma > db_karma_count:
                        # print(f'{user_info[0]}, {user_karma} DB = {db_karma_count}')
                        for i in range(db_karma_count, user_karma):
                            try:
                                db.sync_karma(connection, '-Firekeeper-', flair['user'].name, 'SummonSign')
                            except IntegrityError as err:
                                print(err)


    except Exception as e:
        print(e)
    else:
        print('OMG IT WORKED!!\n\n ! ! SYNCED ! !')


if __name__ == '__main__':
    main()
    # subreddit = reddit.subreddit("SummonSign")
    # print(f'Suspended user 0xdefec8 = {karma.user_is_valid(reddit, subreddit, "0xdefec8")}')
    # print(f'Shadowbanned user Thewalrusworld = {karma.user_is_valid(reddit, subreddit, "Thewalrusworld")}')
    # print(f'Banned user eazeaze = {karma.user_is_valid(reddit, subreddit, "eazeaze")}')
    # print(f'Valid user FOS = {karma.user_is_valid(reddit, subreddit, "FatOldSunbro")}')

