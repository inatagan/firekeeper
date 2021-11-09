from dotenv import load_dotenv
import os
import praw


load_dotenv()
# print(os.environ.get('my_user_agent'))
# print(os.environ.get('my_client_secret'))
reddit = praw.Reddit(
    client_id=os.environ.get('my_client_id'),
    client_secret=os.environ.get('my_client_secret'),
    user_agent=os.environ.get('my_user_agent'),
    username=os.environ.get('my_username'),
    password=os.environ.get('my_password'),
)

subreddit = reddit.subreddit("SummonSign")
for submission in subreddit.new(limit=20):
    for comment in submission.comments:
        print("-*"*20)
        print(comment.body)
