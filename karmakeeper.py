from dotenv import load_dotenv
import os
import praw
import re

# Functions
def getFlair(username):
    # name_formated = f"Redditor(name='{username}')"
    for flair in subreddit.flair():
        try:
            if flair['user'] == str(username):
                user_info = []
                user_info.append(flair['user'])
                user_info.append(flair['flair_text'])
                return user_info[:]
        except Exception as e:
            print(e)



def getKarmaCount(user):
    # karma ??
    karma = 0
    karmaCount = re.findall(r'\d+', str(user[1]).replace(' ', ''))
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
    sub.flair.set(user[0], new_flair_text, user_css)


def syncFlair(sub, user, user_css='green'):
    reddit.subreddit(sub).flair.set(user[0], user[1], user_css)


def alreadyAwarded(award_comment):
    count = 0
    to_user = award_comment.parent().author.name
    from_user = award_comment.author
    submission = award_comment.submission
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
            if not comment.is_root:
                if comment.author == from_user and comment.parent().author.name == to_user:
                    count += 1
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

# retrieval of +karma command
for comment in subreddit.stream.comments(skip_existing=True):
    comment.body.lower()
    # if comment.body == "+karma" or comment.body == "\+karma":
    if comment.body.lower().strip().startswith(("+karma", "\\+karma")) and not comment.is_root:
        if not alreadyAwarded(comment):
            if comment.is_submitter or comment.parent().is_submitter:
                try:
                    user = getFlair(comment.parent().author.name)
                    if len(user) > 0:
                        karma = getKarmaCount(user)
                        user_css = getCSSClass(karma)
                        setFlair(subreddit, user, karma, user_css)
                    else:
                        setFlair(subreddit, comment.parent().author.name, 0, subreddit_css_class[3])
                except:
                    failure_reply = str(f"Sorry /u/{comment.author} you can't do that!!")
                    comment.reply(failure_reply)
                else:
                    print("-*"*20)
                    print(f'by u/{comment.author}')
                    print('SUCCESS')
                    success_reply = str(f"Thank you, /u/{comment.author}! You have awarded karma to user /u/{comment.parent().author.name}!")
                    comment.reply(success_reply)
            else:
                print('ERROR')
