import logging
import os
import praw
import flairsync
import time
from dotenv import load_dotenv
from sqlite3 import IntegrityError
from utils import karma as k
from prawcore.exceptions import PrawcoreException




logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [ %(levelname)s ] | [ %(name)s ]: %(message)s')
log_file_handler = logging.FileHandler('firekeeper.log')
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)




def main():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.environ.get('my_client_id'),
        client_secret=os.environ.get('my_client_secret'),
        user_agent=os.environ.get('my_user_agent'),
        username=os.environ.get('my_username'),
        password=os.environ.get('my_password'),
    )
    my_sub = os.environ.get('my_subreddit')
    subreddit = reddit.subreddit(my_sub)


    running = True
    while running:
        try:
            for comment in subreddit.stream.comments(skip_existing=True):
                if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
                    if comment.is_root:
                        ERROR_TOP_LEVEL = f"F'rgive me /u/{comment.author}, thee can't award +karma from a top leveleth comment!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}."
                        k.moderator_safe_reply(logger, comment, ERROR_TOP_LEVEL)
                    elif not comment.is_submitter and not comment.parent().is_submitter:
                        ERROR_USER_DENIED = f"Ashen one /u/{comment.author}, the *First Flame* quickly fades. Darkness will shortly settle. But one day, tiny flames will dance across the darkness. Like embers, linked by past Lords. Ashen one hearest thou my voice, still?!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}."
                        k.moderator_safe_reply(logger, comment, ERROR_USER_DENIED)
                    elif comment.is_submitter and comment.parent().is_submitter:
                        ERROR_GREEDY_USER = f"F'rgive me /u/{comment.author}, thee can't award +karma to yourself!!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}."
                        k.moderator_safe_reply(logger, comment, ERROR_GREEDY_USER)
                    elif comment.parent().author == '-Firekeeper-':
                        ERROR_FORBIDDEN_USER = f"/u/{comment.author}, my thanks for the +karma thou'st given. But Firekeepers are not meant to have +karma. It is forbidden!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}."
                        k.moderator_safe_reply(logger, comment, ERROR_FORBIDDEN_USER)
                    elif not k.verify_negotiation(comment.author, comment.parent().author, comment, comment.parent()):
                        ERROR_NEGOTIATION_FAIL = f"/u/{comment.author}, the fire fades and the Lords go without thrones. Surrender your fires, to the true heir. Let him grant Death.. to the old gods of Lordran, deliverers of the *First Flame*!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}."
                        k.moderator_safe_reply(logger, comment, ERROR_NEGOTIATION_FAIL)
                    else:
                        try:
                            plat = k.get_platform(comment.submission.title)
                            k.add_karma_to_db(comment.author.name, comment.parent().author.name, comment.link_id, comment.id, comment.submission.title, plat, comment.subreddit.display_name)
                        except IntegrityError:
                            ERROR_ALREADY_AWARDED = f"F'rgive me /u/{comment.author}, thee has't already award'd +karma to *this* us'r!! \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger,comment, ERROR_ALREADY_AWARDED)
                        except Exception:
                            ERROR_UNKNOWN = f"Forgive me /u/{comment.author}, something wenteth wrong!!  \n\n ***  \n Prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger, comment, ERROR_UNKNOWN)
                            logger.exception('THIS CANNOT CONTINUE.. {}'.format(comment.permalink))
                        else:
                            try:
                                flairsync.main(comment.parent().author.name)
                            except Exception:
                                logger.exception('FLAIRSYNC FAILED {}'.format(comment.permalink))
                            SUCCESS_REPLY = f"/u/{comment.author}, my thanks for the +karma thou'st given to us'r /u/{comment.parent().author.name}!  \n\n ***  \n Farewell, ashen one. Mayst thou thy peace discov'r. If thine heart should bend, prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+Firekeeper&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger, comment, SUCCESS_REPLY)
                            if 'close' in comment.body.lower() and comment.is_submitter:
                                post = comment.submission
                                try:
                                    post.mod.flair(text=":sunbro: Duty Fulfilled!", css_class="duty-fulfilled", flair_template_id="25213842-1029-11e6-ba76-0ecc83f85b2b")
                                except:
                                    logger.exception('FAILED TO CLOSE SUBMISSION {}'.format(comment.submission.permalink))
        except KeyboardInterrupt:
            logger.info('Termination received. Goodbye!')
            running = False
        except PrawcoreException as err:
            logger.exception('Oops I did it again.. {} comment? {}'.format(err, comment.permalink))
            time.sleep(10)




if __name__ == '__main__':
    main()

