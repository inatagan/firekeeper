from dotenv import load_dotenv
import os
import praw
from utils import karma
from database import db_init as db


#Load user secret
load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ.get('my_client_id'),
    client_secret=os.environ.get('my_client_secret'),
    user_agent=os.environ.get('my_user_agent'),
    username=os.environ.get('my_username'),
    password=os.environ.get('my_password'),
)


# main
subreddit = reddit.subreddit("SummonSign")
connection = db.connect()
db.create_tables(connection)
try:
    for flair in reddit.subreddit("SummonSign").flair():
        user_info = []
        user_info.append(flair['user'])
        user_info.append(flair['flair_text'])
        user_karma = karma.getKarmaCount(user_info)
        if user_karma > 800:
            k = db.get_user_karma(connection, flair['user'].name)
            # print(flair)
            # user_css = karma.getCSSClass(user_karma)
            # syncFlair(subreddit, user_info, user_css)
            print(f'{user_info[0]}, {user_karma} DB = {k[0]}')
            # for i in range(user_karma):
            #     db.sync_karma(connection, '-Firekeeper-', flair['user'].name, 'SummonSign')
except Exception as e:
    print(e)
else:
    print('SYNCED ! !')
