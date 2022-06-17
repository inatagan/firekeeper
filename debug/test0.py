from re import sub
from dotenv import load_dotenv
import os
import praw
import re


def alreadyAwarded(award_comment):
    count = 0
    to_user = award_comment.parent().author.name
    from_user = award_comment.author
    submission = award_comment.submission
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        # print(comment.body)
        if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
            # if not comment.is_root:
            if comment.parent_id == comment.link_id:
                print(f'comment.is_root {comment.is_root}')
                if comment.author == from_user and comment.parent().author.name == to_user:
                    # print(f'from user {from_user}')
                    # print(f'to user {to_user}')
                    # print(f'comment.author {comment.author}')
                    # print(f'comment.parent().author.name {comment.parent().author.name}')
                    count += 1
    # print(count)
    if count > 1:
        return True
    else:
        return False


load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ.get('my_client_id'),
    client_secret=os.environ.get('my_client_secret'),
    user_agent=os.environ.get('my_user_agent'),
    username=os.environ.get('my_username'),
    password=os.environ.get('my_password'),
)



subreddit = reddit.subreddit("SummonSign")
for comment in subreddit.stream.comments(skip_existing=True):
    comment.body.lower()
    # if comment.body == "+karma" or comment.body == "\+karma":
    if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
        print("-*"*20)
        print(comment.body)
        print(f'by u/{comment.author}')
        print(f'to u/{comment.parent().author.name}')
        # print(f'I D  : {comment.id_from_url}')
        if alreadyAwarded(comment):
            print('duplicated')
        else:
            print('invalid')
