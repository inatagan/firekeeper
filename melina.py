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
log_file_handler = logging.FileHandler('melina.log')
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)




def main():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.environ.get('melina_client_id'),
        client_secret=os.environ.get('melina_client_secret'),
        user_agent=os.environ.get('melina_user_agent'),
        username=os.environ.get('melina_username'),
        password=os.environ.get('melina_password'),
    )
    my_sub = os.environ.get('melina_subreddit')
    my_username = os.environ.get('melina_username')
    subreddit = reddit.subreddit(my_sub)


    running = True
    while running:
        
        
        #multiple streams
        comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)
        mod_log_stream = subreddit.mod.stream.log(pause_after=-1, skip_existing=True)
        modmail_stream = subreddit.mod.stream.modmail_conversations(pause_after=-1, skip_existing=True)
        inbox_stream = reddit.inbox.stream(pause_after=-1, skip_existing=True)
        
        
        try:


            while running:


                for comment in comment_stream:
                    if comment is None:
                        break
                    if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
                        if comment.is_root:
                            ERROR_TOP_LEVEL=f"Foul tarnished /u/{comment.author}, thee can't award +karma from a top level comment!! \n\n ***  \n Good-bye, should you come by a Shabriri Grape, [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_TOP_LEVEL, lock_reply=True)
                        elif not comment.is_submitter and not comment.parent().is_submitter:
                            ERROR_USER_DENIED=f"Unworthy tarnished /u/{comment.author}, I'm searching for my purpose given to me by my mother inside the Erdtree long ago, for the reason that I yet live, burned and bodyless.. I've acted the finger maiden yet I can offer no guidance, I am no maiden. My purpose was long ago lost...  \n\n ***  \n Good-bye, should you come by a Shabriri Grape, [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_USER_DENIED, lock_reply=True)
                        elif comment.is_submitter and comment.parent().is_submitter:
                            ERROR_GREEDY_USER=f"Lowly tarnished /u/{comment.author}, I shall not let you award +karma to yourself!! Destined Death is upon you!  \n\n ***  \n Good-bye, should you come by a Shabriri Grape, [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_GREEDY_USER, lock_reply=True)
                        elif comment.parent().author == '-Melina':
                            ERROR_FORBIDDEN_USER=f"/u/{comment.author}, thank you for the +karma thou'st given. But I am merely playing the role of a maiden and not meant to have +karma. It is forbidden!! \n\n ***  \n Good-bye, should you come by a Shabriri Grape, [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_FORBIDDEN_USER, lock_reply=True)
                        elif not k.verify_negotiation(comment.author, comment.parent().author, comment, comment.parent()):
                            ERROR_NEGOTIATION_FAIL=f"Disgraced /u/{comment.author}! Please put a stop to this madness. The Lord of Frenzied Flame is no lord at all. When the land they preside over is lifeless!! \n\n ***  \n Good-bye, should you come by a Shabriri Grape, [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_NEGOTIATION_FAIL, lock_reply=True)
                        elif k.is_non_participant(comment.parent().author.name):
                            NON_PARTICIPANT_REPLY=f"Tarnished guided by grace /u/{comment.author}, in the name of Queen Marika the Eternal I shall turn your runes into strength!  \n\n ***  \n Good-bye, should you come by a Shabriri Grape, [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=NON_PARTICIPANT_REPLY, lock_reply=True)
                        else:
                            try:
                                plat = k.get_platform(comment.submission.title)
                                k.add_karma_to_db(comment.author.name, comment.parent().author.name, comment.link_id, comment.id, comment.submission.title, plat, comment.subreddit.display_name)
                                # DOUBLE KARMA WEEK
                                k.add_karma_to_db(comment.author.name, comment.parent().author.name, f'{comment.link_id}_DOUBLE', comment.id, comment.submission.title, plat, comment.subreddit.display_name)
                            except IntegrityError:
                                ERROR_ALREADY_AWARDED=f"Foul tarnished /u/{comment.author}, thee has't already award'd +karma to *this* user!! \n\n ***  \n Good-bye, should you come by a Shabriri Grape, [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                                k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_ALREADY_AWARDED, lock_reply=True)
                            except Exception:
                                ERROR_UNKNOWN=f"Forgive me tarnished /u/{comment.author}, something wenteth wrong!!  \n\n ***  \n Prithee [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                                k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_UNKNOWN, lock_reply=True)
                                logger.exception('THIS CANNOT CONTINUE.. {}'.format(comment.permalink))
                            else:
                                try:
                                    flairsync.main(comment.parent().author.name)
                                except Exception:
                                    logger.exception('FLAIRSYNC FAILED {}'.format(comment.permalink))
                                SUCCESS_REPLY=f"Tarnished guided by grace /u/{comment.author}, in the name of Queen Marika the Eternal I shall grant +karma to user /u/{comment.parent().author.name}!  \n\n ***  \n Good-bye, should you come by a Shabriri Grape, [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+the+false+maiden&message=) of /r/{subreddit}."
                                k.moderator_safe_reply(logger=logger, comment=comment, message=SUCCESS_REPLY, lock_reply=True)
                                if any(word in comment.body.lower() for word in ('close', 'complete', 'thanks', 'gg')) and comment.is_submitter:
                                    post = comment.submission
                                    try:
                                        post.mod.flair(text=":sunbro: Duty Fulfilled!", css_class="duty-fulfilled", flair_template_id="186b0ec2-9343-11ec-b414-cefd332e8238")
                                    except:
                                        logger.exception('FAILED TO CLOSE SUBMISSION {}'.format(comment.submission.permalink))
                                # DOUBLE WEEK REPLY, REMOVE AFTER END
                                k.moderator_safe_reply(logger=logger, comment=comment, message=SUCCESS_REPLY, lock_reply=True)
                
                
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
                

                for modmail in modmail_stream:
                    if modmail is None:
                        break
                    if any(subject in modmail.subject.lower() for subject in ("about the false maiden", "about+the+false+maiden")):
                        conversation = subreddit.modmail(modmail.id, mark_read=True)
                        for message in conversation.messages:
                            if any(shabriri_grape in message.body_markdown.lower() for shabriri_grape in ("shabriri", "grape", "have", "one")):
                                try:
                                    modmail.reply(body=f"Disgraced /u/{message.author}! *You...* have inherited the Frenzied Flame. A pity. You are no longer fit. Our journey together ends here. And remember... Should you rise as the Lord of Chaos, I will kill you, as sure as night follows day. Such is my duty, for allowing you the strength of runes. Goodbye, my companion. Goodbye, Torrent... I will seek you, as far as you may travel... To deliver you what is yours. **Destined Death**. \n\n *** \n I am a bot, and this action was performed automatically.", author_hidden=False)
                                except:
                                    logger.exception('FAIL TO REPLY MODMAIL: {}'.format(modmail.id))


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
                            comment = reddit.comment(url=item.body)
                            try:
                                k.delete_karma_by_comment_id(comment.id, my_username, reddit)
                            except:
                                logger.exception('FAIL TO DELETE COMMENT_KARMA: {}'.format(comment.permalink))
                            else:
                                item.reply(body=f"SUCCESS: karma deleted: \n\n{comment.permalink}")




        except KeyboardInterrupt:
            logger.info('Termination received. Goodbye!')
            running = False
        except PrawcoreException as err:
            logger.exception('Oops I did it again.. ERROR= {}'.format(err))
            time.sleep(10)




if __name__ == '__main__':
    main()

