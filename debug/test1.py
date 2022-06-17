from dotenv import load_dotenv
import os
import praw
import re


# Functions
def getFlair(username):
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


def syncFlair(sub, user, user_css='green'):
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
# comment = reddit.comment("ibrzhma")
# comment = reddit.comment("ibaafue")
# print(type(comment.parent().author_flair_text))
# print(comment.parent().author_flair_css_class)

# print(subreddit.flair(redditor='Str4wH4tLuffym'))
# userflair = subreddit.flair(redditor='Str4wH4tLuffym')
# for item in userflair:
#     print(item)
# for key, item in enumerate(subreddit.flair(redditor='Str4wH4tLuffym')):
#     print(f'{item}\n')



user1 = getFlair('maxuzumakiz')
print(f'username = {user1[0]}')
print(f'userflair is none = {user1[1] is None}')
print(f'userflair == none = {user1[1] == None}')
print(f'userflair is NOT none = {user1[1] is not None}')
print(f'userflair != NOT none = {user1[1] != None}')
if user1[1] is not None:
    print(f'NOT NONE')
    if len(user1[1] > 0):
        print('NOT NONE and NOT 0')
    else:
        print('NOT NONE and 0')
print(f'css is NOT none = {user1[2] is not None}')
print(f'css != none = {user1[2] != None}')
print(f'user OBJECT = {user1}')
print('+'*12)
user1 = getFlair('fatoldsunbro')
print(f'username = {user1[0]}')
print(f'userflair is none = {user1[1] is None}')
print(f'userflair == none = {user1[1] == None}')
print(f'userflair LEN none = {len(user1[1])}')
print(f'userflair is NOT none = {user1[1] is not None}')
print(f'userflair != NOT none = {user1[1] != None}')
if user1[1] is not None:
    print(f'NOT NONE')
    if len(user1[1]) > 0:
        print('NOT NONE and NOT 0')
    else:
        print('NOT NONE and 0')
print(f'css is NOT none = {user1[2] is not None}')
print(f'css != none = {user1[2] != None}')
print(f'user OBJECT = {user1}')
print('+'*12)

# user2 = getFlair('Str4wH4tLuffym')
# print('Str4wH4tLuffym len:')
# print(len(user2))
# print(user2)

# print(subreddit.flair(redditor='Str4wH4tLuffym'))


# retrieval of +karma command
# for comment in subreddit.stream.comments(skip_existing=True):
#     comment.body.lower()
#     if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
#         if comment.is_root:
#             bot_reply = comment.reply(f"F'rgive me /u/{comment.author}, thee can't award +karma from a top leveleth comment!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
#             bot_reply.mod.distinguish(how="yes")
#             bot_reply.mod.lock()
#         elif not comment.is_submitter and not comment.parent().is_submitter:
#             bot_reply = comment.reply(f"Ashen one /u/{comment.author}, hearest thou my voice, still?!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
#             bot_reply.mod.distinguish(how="yes")
#             bot_reply.mod.lock()
#         elif comment.is_submitter and comment.parent().is_submitter:
#             bot_reply = comment.reply(f"F'rgive me /u/{comment.author}, thee can't award +karma to yourself!!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
#             bot_reply.mod.distinguish(how="yes")
#             bot_reply.mod.lock()
#         elif comment.parent().author == '-Firekeeper-':
#             bot_reply = comment.reply(f"/u/{comment.author}, my thanks for the +karma thou'st given. But Firekeepers are not meant to have +karma. It is forbidden!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
#             bot_reply.mod.distinguish(how="yes")
#             bot_reply.mod.lock()
#         elif alreadyAwarded(comment):
#             bot_reply = comment.reply(f"F'rgive me /u/{comment.author}, thee has't already award'd +karma to *this* us'r!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
#             bot_reply.mod.distinguish(how="yes")
#             bot_reply.mod.lock() 
#         else:
#             try:
#                 user = getFlair(comment.parent().author.name)
#                 if len(user) > 0:
#                     karma = getKarmaCount(user)
#                     user_css = getCSSClass(karma)
#                     setFlair(subreddit, user, karma, user_css)
#                 else:
#                     setFlair(subreddit, comment.parent().author.name, 0, subreddit_css_class[3])
#             except:
#                 bot_reply = comment.reply(f"Forgive me /u/{comment.author}, something wenteth wrong!!  \n\n ***  \n Prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
#                 bot_reply.mod.distinguish(how="yes")
#                 bot_reply.mod.lock()
#             else:
#                 bot_reply = comment.reply(f"/u/{comment.author}, my thanks for the +karma thou'st given to us'r /u/{comment.parent().author.name}!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
#                 bot_reply.mod.distinguish(how="yes")
#                 bot_reply.mod.lock()
#                 if 'close' in comment.body.lower() and comment.is_submitter:
#                     post = comment.submission
#                     post.mod.flair(text=":sunbro: Duty Fulfilled!", css_class="duty-fulfilled", flair_template_id="186b0ec2-9343-11ec-b414-cefd332e8238")

