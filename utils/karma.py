import re
from prawcore.exceptions import NotFound


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


# class Karma:
#     def __init__(self, from_user='-Firekeeper-', to_user, submission_id=None, submission_title, subreddit, date):
#         self.from_user = from_user
#         self.to_user = to_user
#         self.submission_id = submission_id
#         self.submission_title = submission_title
#         self.platform = getPlatform(self)
#         self.subreddit = subreddit
#         self.date = date


def getFlair(username, subreddit):
    user_info = []
    try:
        for flair in subreddit.flair(redditor=username):
            user_info.append(flair['user'])
            user_info.append(flair['flair_text'])
            user_info.append(flair['flair_css_class'])
    except Exception as e:
            print(e)
    finally:
            return user_info[:]


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


def syncFlair(reddit, sub, user, user_css='green'):
    reddit.subreddit(sub).flair.set(user[0], user[1], user_css)


def alreadyAwarded(award_comment):
    count = 0
    to_user = award_comment.parent().author
    from_user = award_comment.author
    submission = award_comment.submission
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
            if not comment.is_root:
                if comment.author == from_user and comment.parent().author == to_user:
                    count += 1
    if count > 1:
        return True
    else:
        return False


def getPlatform(submission_title):
    if 'ps4' in str(submission_title).lower():
        return 'ps4'
    if 'ps5' in str(submission_title).lower():
        return 'ps5'
    if 'psx' in str(submission_title).lower():
        return 'psx'
    if 'xbox' in str(submission_title).lower():
        return 'xbox'
    if 'pc' in str(submission_title).lower():
        return 'pc'


def user_is_banned(subreddit, username):
    return any(subreddit.banned(redditor=username))


def user_exists(reddit, username):
    try:
        reddit.redditor(username).id
    except (NotFound, AttributeError):
        return False
    return True


def user_is_valid(reddit, subreddit, username):
    try:
        reddit.redditor(username).id
    except (NotFound, AttributeError):
        return False
    else:
        return not any(subreddit.banned(redditor=username))

