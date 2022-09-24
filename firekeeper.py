import logging
import os
import praw
import flairsync
import time
from dotenv import load_dotenv
from sqlite3 import IntegrityError
from utils import karma as k
from prawcore.exceptions import PrawcoreException
from praw.models import Message




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
    my_username = os.environ.get('my_username')
    subreddit = reddit.subreddit(my_sub)


    #multiple streams
    comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)
    mod_log_stream = subreddit.mod.stream.log(pause_after=-1, skip_existing=True)
    # modmail_stream = subreddit.mod.stream.modmail_conversations(pause_after=-1, skip_existing=True)
    inbox_stream = reddit.inbox.stream(pause_after=-1, skip_existing=True)


    running = True
    while running:
        try:
            for comment in comment_stream:
                if comment is None:
                    break
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


            for log in mod_log_stream:
                if log is None:
                    break
                if log.action == "removelink":
                    try:
                        submission = reddit.submission(url=f"https://www.reddit.com{log.target_permalink}")
                    except:
                        logger.exception('FAIL TO RETRIEVE PERMALINK: {}'.format(log.target_permalink))
                    else:
                        k.submission_clear(submission, my_username, logger)
                if log.action == "banuser" and log.details == "permanent":
                    try:
                        k.add_non_participant_to_db(log.target_author, subreddit.display_name)
                    except:
                        logger.exception('FAIL TO ADD TO DB_NON_PARTICIPANT: {}'.format(log.target_author))
                    try:
                        subreddit.flair.set(log.target_author, text="quarantined", css_class="red")
                    except:
                        logger.exception('FAIL TO SET USERFLAIR: {}'.format(log.target_author))
            

            # for modmail in modmail_stream:
            #     if modmail is None:
            #         break
            #     if "about the false maiden" in modmail.subject.lower() or "about+the+false+maiden" in modmail.subject.lower():
            #         conversation = subreddit.modmail(modmail.id, mark_read=True)
            #         for message in conversation.messages:
            #             if "shabriri grape" in message.body_markdown.lower():
            #                 try:
            #                     modmail.reply(body=f"Disgraced /u/{message.author}! *You...* have inherited the Frenzied Flame. A pity. You are no longer fit. Our journey together ends here. And remember... Should you rise as the Lord of Chaos, I will kill you, as sure as night follows day. Such is my duty, for allowing you the strength of runes. Goodbye, my companion. Goodbye, Torrent... I will seek you, as far as you may travel... To deliver you what is yours. **Destined Death**.", author_hidden=False)
            #                 except:
            #                     logger.exception('FAIL TO REPLY MODMAIL: {}'.format(modmail.id))


            for item in inbox_stream:
                if item is None:
                    break
                if isinstance(item, Message):
                    if 'add non participant' in item.subject:
                        username = item.body
                        try:
                            k.add_non_participant_to_db(username, subreddit.display_name)
                        except IntegrityError:
                            item.reply(body=f"FAIL: u/{username} already is non participant")
                        except:
                            item.reply(body=f"FAIL: u/{username} SOMETHING WENT WRONG!!")
                            logger.exception('FAIL TO ADD NON PARTIPANT: {}'.format(username))
                        else:
                            item.reply(body=f"SUCCESS: u/{username} added to non participant")
                    if 'remove non participant' in item.subject:
                        username = item.body
                        try:
                            k.remove_non_participant_to_db(username, subreddit.display_name)
                        except:
                            item.reply(body=f"FAIL: u/{username} SOMETHING WENT WRONG!!")
                            logger.exception('FAIL TO ADD NON PARTIPANT: {}'.format(username))
                        else:
                            item.reply(body=f"SUCCESS: u/{username} removed from non participant")
                    if 'thread clear' in item.subject:
                        try:
                            submission = reddit.submission(url=f"{item.body}")
                        except:
                            logger.exception('FAIL TO RETRIEVE PERMALINK: {}'.format(log.target_permalink))
                        else:
                            k.submission_clear(submission, my_username, logger)
                            item.reply(body=f"SUCCESS: submission cleaned: {submission.permalink}")
                    if 'sync karma' in item.subject:
                        info = []
                        for data in item.body.split(","):
                            info.append(data.strip())
                        try:
                            k.sync_karma_to_db(username=info[0],karma=int(info[1]), platform=info[2], subreddit=subreddit.display_name)
                        except:
                            logger.exception('FAIL TO SYNC USER_KARMA: {}'.format(info))
                        else:
                            item.reply(body=f"SUCCESS: u/{info[0]} flair updated!!")
                            subreddit.modmail.create(subject="karma exchange", body="karma exchange complete.\n\n---", recipient=info[0])
                    if 'delete all karma' in item.subject:
                        username = item.body
                        try:
                            k.delete_all_karma_from_user(username)
                        except:
                            logger.exception('FAIL TO DELETE USER_KARMA: {}'.format(username))
                        else:
                            item.reply(body=f"SUCCESS: u/{item.body} karma deleted!!")
                    if 'delete karma by comment' in item.subject:
                        comment_id = item.body
                        try:
                            k.delete_karma_by_comment_id(comment_id, my_username, reddit)
                        except:
                            logger.exception('FAIL TO DELETE COMMENT_KARMA: {}'.format(comment_id))
                        else:
                            comment = reddit.comment(comment_id)
                            item.reply(body=f"SUCCESS: karma deleted: \n\n{comment.permalink}")




        except KeyboardInterrupt:
            logger.info('Termination received. Goodbye!')
            running = False
        except PrawcoreException as err:
            logger.exception('Oops I did it again.. {} comment? {}'.format(err, comment.permalink))
            time.sleep(10)




if __name__ == '__main__':
    main()

