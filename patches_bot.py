from dotenv import load_dotenv
import os
import praw
import re


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


def getCommentFlair(comment):
    user_info = []
    try:
        user_info.append(comment.author.name)
        user_info.append(comment.author_flair_text)
        user_info.append(comment.author_flair_css_class)
    except Exception as e:
        print(e)
    finally:
        return user_info[:]


def getKarmaCount(user):
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


load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ.get('my_client_id'),
    client_secret=os.environ.get('my_client_secret'),
    user_agent=os.environ.get('my_user_agent'),
    username=os.environ.get('my_username'),
    password=os.environ.get('my_password'),
)


def main():
    subreddit = reddit.subreddit("PatchesEmporium")
    for comment in subreddit.stream.comments(skip_existing=True):
        comment.body.lower()
        if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
            if comment.is_root:
                bot_reply = comment.reply(f"Oi /u/{comment.author} just hold your horses a moment, you can't award +karma from a top level comment!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif not comment.is_submitter and not comment.parent().is_submitter:
                bot_reply = comment.reply(f"Stingy little beggar /u/{comment.author}, you can't do that. Try to find it in your heart next time, eh?!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif comment.is_submitter and comment.parent().is_submitter:
                bot_reply = comment.reply(f"Shame on you, you insatiable wench /u/{comment.author}, you can't award +karma to yourself greedy guts!!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif comment.parent().author == 'Totally-not-Patches':
                bot_reply = comment.reply(f"Sorry /u/{comment.author} are you a cleric or something? And you are trying to award +karma to the wrong user!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif alreadyAwarded(comment):
                bot_reply = comment.reply(f"Thought you could outwit an onion? /u/{comment.author} you have already awarded +karma to *this* user!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock() 
            else:
                try:
                    user = getCommentFlair(comment.parent())
                    if user[2] is not None:
                        karma = getKarmaCount(user)
                        user_css = getCSSClass(karma)
                        setFlair(subreddit, user, karma, user_css)
                    else:
                        setFlair(subreddit, user, 0)
                except:
                    bot_reply = comment.reply(f"Shame on you, you rotten cleric /u/{comment.author} something went wrong! But I'll forgive you. View it as a learning experience. At any rate, it's nice just to see you safe!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock()
                else:
                    bot_reply = comment.reply(f"Cheers for that! /u/{comment.author} you have awarded +karma to user /u/{comment.parent().author.name}!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock()
                    if 'close' in comment.body.lower() and comment.is_submitter:
                        post = comment.submission
                        post.mod.flair(text="Complete!", css_class="duty-fulfilled", flair_template_id="a9bcc130-9a8d-11ec-820c-aa2f5c846ca8")


if __name__ == '__main__':
    main()

