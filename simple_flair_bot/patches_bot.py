from dotenv import load_dotenv
import os
import praw
import re




def get_comment_flair(comment):
    user_info = []
    try:
        user_info.append(comment.author.name)
        user_info.append(comment.author_flair_text)
        user_info.append(comment.author_flair_css_class)
    except Exception as e:
        print(e)
    finally:
        return user_info[:]


def get_karma_count(user):
    karma = 0
    karmaCount = re.findall(r'\d+', str(user[1]).replace(' ', ''))
    for i in karmaCount:
        karma = int(i)
    return karma


def get_css_class(karma):
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


def set_flair(sub, user, karma, user_css='green'):
    newKarma = karma + 1
    new_flair_text = str(f'+{newKarma} Karma')
    sub.flair.set(user[0], text=new_flair_text, css_class=user_css)


def already_awarded(award_comment):
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


def check_command(comment):
    if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
        return True
    return False


def verify_negotiation(user_from, user_to, comment, parent_comment):
    current_comment = comment
    found_from = False
    found_to = False
    post_list = []
    submission_author_name = "Totally-not-Patches" if current_comment.submission.author is None else current_comment.submission.author.name
    if submission_author_name == user_from.name and submission_author_name != user_to.name and not check_command(parent_comment):
        return True #the OP can send to anyone
    parent_comment.submission.comments.replace_more(limit=None)
    namelist = []
    for cmnt in parent_comment.submission.comments.list():
        if cmnt.author is not None and cmnt.id != comment.id and cmnt.author.name == user_from.name and not check_command(cmnt):
            namelist.append(cmnt.author.name)
    if user_from.name in namelist:
        post_list.append(user_from.name)
    while not current_comment.is_root:
        current_comment = current_comment.parent()
        if current_comment.author is not None:
            post_list.append(current_comment.author.name)
    post_list.append(submission_author_name)
    if len(post_list) > 1 and user_to and user_from and hasattr( user_to, "name") and hasattr(user_from, "name"):
        pl = list(reversed(post_list))
        for n in range(len(post_list)):
            if n and pl[n] == user_from.name and pl[n - 1] == user_to.name:
                found_to = True
            if n and pl[n] == user_to.name and pl[n - 1] == user_from.name:
                found_from = True
    return (found_from and found_to)




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
    client_id=os.environ.get('patches_client_id'),
    client_secret=os.environ.get('patches_client_secret'),
    user_agent=os.environ.get('patches_user_agent'),
    username=os.environ.get('patches_username'),
    password=os.environ.get('patches_password'),
)


def main():
    subreddit = reddit.subreddit("PatchesEmporium")
    for comment in subreddit.stream.comments(skip_existing=True):
        if check_command(comment):
            if comment.is_root:
                bot_reply = comment.reply(body=f"Oi /u/{comment.author} just hold your horses a moment, you can't award +karma from a top level comment!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif not comment.is_submitter and not comment.parent().is_submitter:
                bot_reply = comment.reply(body=f"Stingy little beggar /u/{comment.author}, you can't do that. Try to find it in your heart next time, eh?!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif comment.is_submitter and comment.parent().is_submitter:
                bot_reply = comment.reply(body=f"Shame on you, you insatiable wench /u/{comment.author}, you can't award +karma to yourself greedy guts!!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif comment.parent().author == 'Totally-not-Patches':
                bot_reply = comment.reply(body=f"Sorry /u/{comment.author} are you a cleric or something? And you are trying to award +karma to the wrong user!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif already_awarded(comment):
                bot_reply = comment.reply(body=f"Thought you could outwit an onion? /u/{comment.author} you have already awarded +karma to *this* user!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock() 
            elif not verify_negotiation(comment.author, comment.parent().author, comment, comment.parent()):
                bot_reply = comment.reply(body=f"Thought you could outwit an onion? /u/{comment.author} I see no evidence that a trade has ocurred!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock() 
            else:
                try:
                    user = get_comment_flair(comment.parent())
                    if user[2] is not None:
                        karma = get_karma_count(user)
                        user_css = get_css_class(karma)
                        set_flair(subreddit, user, karma, user_css)
                    else:
                        set_flair(subreddit, user, 0)
                except:
                    bot_reply = comment.reply(body=f"Shame on you, you rotten cleric /u/{comment.author} something went wrong! But I'll forgive you. View it as a learning experience. At any rate, it's nice just to see you safe!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock()
                else:
                    bot_reply = comment.reply(body=f"Cheers for that! /u/{comment.author} you have awarded +karma to user /u/{comment.parent().author.name}!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock()
                    if 'close' in comment.body.lower() and comment.is_submitter:
                        post = comment.submission
                        post.mod.flair(text="Complete!", css_class="duty-fulfilled", flair_template_id="a9bcc130-9a8d-11ec-820c-aa2f5c846ca8")


if __name__ == '__main__':
    main()

