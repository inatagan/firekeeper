from dotenv import load_dotenv
import os
import praw
from utils import karma as k
from database import db_init as db
from sqlite3 import IntegrityError
import flairsync


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
def main():
    subreddit = reddit.subreddit("BeyondTheFog")
    # retrieval of +karma command
    for comment in subreddit.stream.comments(skip_existing=True):
        comment.body.lower()
        if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
            if comment.is_root:
                bot_reply = comment.reply(f"F'rgive me /u/{comment.author}, thee can't award +karma from a top leveleth comment!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif not comment.is_submitter and not comment.parent().is_submitter:
                bot_reply = comment.reply(f"Ashen one /u/{comment.author}, hearest thou my voice, still?!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif comment.is_submitter and comment.parent().is_submitter:
                bot_reply = comment.reply(f"F'rgive me /u/{comment.author}, thee can't award +karma to yourself!!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()
            elif comment.parent().author == '-Firekeeper-':
                bot_reply = comment.reply(f"/u/{comment.author}, my thanks for the +karma thou'st given. But Firekeepers are not meant to have +karma. It is forbidden!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
                bot_reply.mod.distinguish(how="yes")
                bot_reply.mod.lock()


            # elif alreadyAwarded(comment):
            #     bot_reply = comment.reply(f"F'rgive me /u/{comment.author}, thee has't already award'd +karma to *this* us'r!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
            #     bot_reply.mod.distinguish(how="yes")
            #     bot_reply.mod.lock() 


            else:
                try:
                    # user = k.getCommentFlair(comment.parent())
                    connection = db.connect()
                    db.create_tables(connection)
                    plat = k.getPlatform(comment.submission.title)
                    db.add_karma(connection, comment.author.name, comment.parent().author.name, comment.link_id, comment.submission.title, plat, comment.subreddit.display_name)
                    # if user[2] is not None:
                    #     karma = k.getKarmaCount(user)
                    #     user_css = getCSSClass(karma)
                    #     setFlair(subreddit, user, karma, user_css)
                    # else:
                    #     setFlair(subreddit, user, 0)
                except IntegrityError:
                    bot_reply = comment.reply(f"F'rgive me /u/{comment.author}, thee has't already award'd +karma to *this* us'r!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock() 

                except:
                    bot_reply = comment.reply(f"Forgive me /u/{comment.author}, something wenteth wrong!!  \n\n ***  \n Prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock()
                else:

                    flairsync.main(comment.parent().author.name)

                    bot_reply = comment.reply(f"/u/{comment.author}, my thanks for the +karma thou'st given to us'r /u/{comment.parent().author.name}!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}.")
                    bot_reply.mod.distinguish(how="yes")
                    bot_reply.mod.lock()
                    if 'close' in comment.body.lower() and comment.is_submitter:
                        post = comment.submission
                        post.mod.flair(text=":sunbro: Duty Fulfilled!", css_class="duty-fulfilled", flair_template_id="186b0ec2-9343-11ec-b414-cefd332e8238")


if __name__ == '__main__':
    main()

