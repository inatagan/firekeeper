from re import sub
from dotenv import load_dotenv
import os
import praw
import re

# Functions
def getFlair(username):
    for flair in subreddit.flair():
        if flair['user'] == username:
            user_info = []
            user_info.append(flair['user'])
            user_info.append(flair['flair_text'])
            return user_info


def getKarmaCount(user):
    karmaCount = re.findall(r'\d+', str(user[1]).replace(' ', ''))
    karma = 0
    for i in karmaCount:
        karma = int(i)
    return karma


def getCSSClass(karma):
    if karma >= 1000:
        user_css = subreddit_css_class[8]
    elif karma >= 500:
        user_css = subreddit_css_class[7]
    elif karma >= 250:
        user_css = subreddit_css_class[6]
    elif karma >= 100:
        user_css = subreddit_css_class[5]
    elif karma >= 50:
        user_css = subreddit_css_class[4]
    elif karma >= 15:
        user_css = subreddit_css_class[3]
    else:
        user_css = subreddit_css_class[2]
    return user_css


def setFlair(sub, user, karma, user_css='green'):
    newKarma = karma + 1
    new_flair_text = str(f'+{newKarma} Karma')
    # reddit.subreddit(sub).flair.set(user[0], new_flair_text, user_css)
    sub.flair.set(user[0], new_flair_text, user_css)


def syncFlair(sub, user, user_css='green'):
    sub.flair.set(user[0], user[1], user_css)


def alreadyAwarded(award_comment):
    count = 0
    to_user = award_comment.parent().author.name
    from_user = award_comment.author
    submission = award_comment.submission
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        # print(comment.body)
        if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
            if not comment.is_root:
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


#Tuple containing subreddit valid css_class
subreddit_css_class = (
    "red",
    "mod",
    "green",
    "green tier2",
    "green tier3",
    "green tier4",
    "green tier5",
    "green tier6",
    "green tier7"
)


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
subreddit = reddit.subreddit("BeyondTheFog")

try:
    for flair in reddit.subreddit("SummonSign").flair():
        user_info = []
        user_info.append(flair['user'])
        user_info.append(flair['flair_text'])
        user_karma = getKarmaCount(user_info)
        if user_karma > 1:
            user_css = getCSSClass(user_karma)
            syncFlair(subreddit, user_info, user_css)
            print(user_info[0], user_karma, user_css)
except Exception as e:
    print(e)
else:
    print('SYNCED ! !')
