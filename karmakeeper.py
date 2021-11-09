from re import sub
from dotenv import load_dotenv
import os
import praw

load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ.get('my_client_id'),
    client_secret=os.environ.get('my_client_secret'),
    user_agent=os.environ.get('my_user_agent'),
    username=os.environ.get('my_username'),
    password=os.environ.get('my_password'),
)

subreddit = reddit.subreddit("SummonSign")

# retrieval of +karma command
# for comment in subreddit.stream.comments(skip_existing=True):
#     comment.body.lower()
#     if comment.body == "+karma" or comment.body == "\+karma":
#         print("-*"*20)
#         print(comment.body)
#         print(f'by u/{comment.author}')

# for template in subreddit.flair.templates:
#     print(template)
# TODO - use regex to extract current karma count
# for flair in subreddit.flair():
#     print(flair)