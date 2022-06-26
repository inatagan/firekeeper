from dotenv import load_dotenv
import os
import praw
from utils import karma
import sys


#Load user secret
load_dotenv('.env_flairsync')
reddit = praw.Reddit(
    client_id=os.environ.get('my_client_id'),
    client_secret=os.environ.get('my_client_secret'),
    user_agent=os.environ.get('my_user_agent'),
    username=os.environ.get('my_username'),
    password=os.environ.get('my_password'),
)


def main():
    try:
        username = sys.argv[1]
    except IndexError:
        print("Error: Missing Arguments!")
    else:
        user = karma.getUserFromDB(username)
        sub_list = ('SummonSign', 'BeyondTheFog')
        for sub in sub_list:
            karma.syncFlairFromDB(reddit, sub, user)


if __name__ == '__main__':
    main()

