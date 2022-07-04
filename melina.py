from dotenv import load_dotenv
import os
import praw
from utils import karma as k
from sqlite3 import IntegrityError
import flairsync


load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ.get('melina_client_id'),
    client_secret=os.environ.get('melina_client_secret'),
    user_agent=os.environ.get('melina_user_agent'),
    username=os.environ.get('melina_username'),
    password=os.environ.get('melina_password'),
)


def main():
    subreddit = reddit.subreddit("BeyondTheFog")
    for comment in subreddit.stream.comments(skip_existing=True):
        if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
            if comment.is_root:
                bot_reply = comment.reply(body=f"Foul tarnished /u/{comment.author}, thee can't award +karma from a top level comment!! \n\n ***  \n Good-bye, should you come by the Frenzied Flame, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif not comment.is_submitter and not comment.parent().is_submitter:
                bot_reply = comment.reply(body=f"Foul tarnished /u/{comment.author}, My purpose was given to me by my mother. But now, I act of my own volition. I have set my heart upon the world that I would have. Regardless of my mother's designs. I won't allow anyone to speak ill of that. Not even you!  \n\n ***  \n Good-bye, should you come by the Frenzied Flame, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif comment.is_submitter and comment.parent().is_submitter:
                bot_reply = comment.reply(body=f"Lowly tarnished /u/{comment.author}, I shall not let you award +karma to yourself!! Destined Death is upon you!  \n\n ***  \n Good-bye, should you come by the Frenzied Flame, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif comment.parent().author == '-Melina':
                bot_reply = comment.reply(body=f"/u/{comment.author}, thank you for the +karma thou'st given. But I am merely playing the role of a maiden and not meant to have +karma. It is forbidden!! \n\n ***  \n Good-bye, should you come by the Frenzied Flame, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            else:
                try:
                    plat = k.get_platform(comment.submission.title)
                    k.add_karma_to_db(comment.author.name, comment.parent().author.name, comment.link_id, comment.id, comment.submission.title, plat, comment.subreddit.display_name)
                except IntegrityError:
                    bot_reply = comment.reply(body=f"Fouls tarnished /u/{comment.author}, thee has't already award'd +karma to *this* user!! \n\n ***  \n Good-bye, should you come by the Frenzied Flame, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock() 
                except Exception:
                    bot_reply = comment.reply(body=f"Forgive me tarnished /u/{comment.author}, something wenteth wrong!!  \n\n ***  \n Prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock()
                else:
                    flairsync.main(comment.parent().author.name)
                    bot_reply = comment.reply(body=f"Tarnished guided by grace /u/{comment.author}, in the name of Queen Marika the Eternal I shall grant +karma to user /u/{comment.parent().author.name}!  \n\n ***  \n Good-bye, should you come by the Frenzied Flame, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock()
                    if 'close' in comment.body.lower() and comment.is_submitter:
                        post = comment.submission
                        post.mod.flair(text=":sunbro: Duty Fulfilled!", css_class="duty-fulfilled", flair_template_id="186b0ec2-9343-11ec-b414-cefd332e8238")


if __name__ == '__main__':
    main()

