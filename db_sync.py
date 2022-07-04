from dotenv import load_dotenv
import os
import praw
from utils import karma
from database import db_init as db
from sqlite3 import IntegrityError
from progress.bar import ShadyBar
from progress.spinner import LineSpinner




load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ.get('my_client_id'),
    client_secret=os.environ.get('my_client_secret'),
    user_agent=os.environ.get('my_user_agent'),
    username=os.environ.get('my_username'),
    password=os.environ.get('my_password'),
)


def main():


    subreddit = reddit.subreddit("BeyondTheFog")
    connection = db.connect()
    db.create_tables(connection)
    flair_list = {}
    spinner = LineSpinner('Loading.. ')
    
    
    for flair in subreddit.flair():
        # Use the command bellow to create an quick and dirty flair list for reference:
        # unbuffer python3 db_sync.py 2>&1 | tee -a sub_flair_list.log
        # tup = (flair['user'].name, flair['flair_text'])
        # print(tup)


        key = flair['user'].name
        value = flair['flair_text']
        flair_list[key] = value
        spinner.next()
    
    
    for key, value in ShadyBar('Processing').iter(flair_list.items()):
        if not karma.user_is_valid(reddit, subreddit, key):
            print(f"userflair deleted: {key} : {value}")
            try:
                subreddit.flair.delete(redditor=key)
            except Exception as err:
                print(f'flair removal failed: {err}')
        else:
            user_karma = karma.get_karma_from_dict(value)
            if user_karma > 1:
                db_karma_count = db.get_user_karma(connection, key)
                if user_karma > db_karma_count:
                    for i in range(db_karma_count, user_karma):
                        try:
                            db.sync_karma(connection, '-Firekeeper-', key, subreddit.display_name)
                        except IntegrityError as err:
                            print(err)
                    print(f"userflair synced: {key} : {value}")
    print('OMG IT WORKED!!\n\n ! ! SYNCED ! !')


if __name__ == '__main__':
    main()


