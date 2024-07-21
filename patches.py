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
log_file_handler = logging.FileHandler('patches.log')
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)




def main():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.environ.get('patches_client_id'),
        client_secret=os.environ.get('patches_client_secret'),
        user_agent=os.environ.get('patches_user_agent'),
        username=os.environ.get('patches_username'),
        password=os.environ.get('patches_password'),
    )
    my_sub = os.environ.get('patches_subreddit')
    my_username = os.environ.get('patches_username')
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
                            ERROR_TOP_LEVEL=f"Oi /u/{comment.author} just hold your horses a moment, you can't award +karma from a top level comment!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_TOP_LEVEL, lock_reply=True)
                        elif not comment.is_submitter and not comment.parent().is_submitter:
                            ERROR_USER_DENIED=f"Stingy little beggar /u/{comment.author}, you can't do that. Try to find it in your heart next time, eh?!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_USER_DENIED, lock_reply=True)
                        elif comment.is_submitter and comment.parent().is_submitter:
                            ERROR_GREEDY_USER=f"Shame on you, you insatiable wench /u/{comment.author}, you can't award +karma to yourself greedy guts!!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_GREEDY_USER, lock_reply=True)
                        elif comment.parent().author == '-Melina':
                            ERROR_FORBIDDEN_USER=f"Sorry /u/{comment.author} are you a cleric or something? And you are trying to award +karma to the wrong user!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_FORBIDDEN_USER, lock_reply=True)
                        elif not k.verify_negotiation(comment.author, comment.parent().author, comment, comment.parent()):
                            ERROR_NEGOTIATION_FAIL=f"Thought you could outwit an onion? /u/{comment.author} I see no evidence that a trade has ocurred!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_NEGOTIATION_FAIL, lock_reply=True)
                        elif k.is_non_participant(comment.parent().author.name):
                            NON_PARTICIPANT_REPLY=f"Cheers for that! /u/{comment.author} you have awarded +karma!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                            k.moderator_safe_reply(logger=logger, comment=comment, message=NON_PARTICIPANT_REPLY, lock_reply=True)
                        else:
                            try:
                                plat = k.get_platform(comment.submission.title)
                                k.add_karma_to_db(comment.author.name, comment.parent().author.name, comment.link_id, comment.id, comment.submission.title, plat, comment.subreddit.display_name)

                                # TRIPLE KARMA WEEK
                                k.add_karma_to_db(comment.author.name, comment.parent().author.name, f'{comment.link_id}_DOUBLE', comment.id, comment.submission.title, plat, comment.subreddit.display_name)
                                k.add_karma_to_db(comment.author.name, comment.parent().author.name, f'{comment.link_id}_TRIPLE', comment.id, comment.submission.title, plat, comment.subreddit.display_name)

                            except IntegrityError:
                                ERROR_ALREADY_AWARDED=f"Thought you could outwit an onion? /u/{comment.author} you have already awarded +karma to *this* user!! \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                                k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_ALREADY_AWARDED, lock_reply=True)
                            except Exception:
                                ERROR_UNKNOWN=f"Shame on you, you rotten cleric /u/{comment.author} something went wrong! But I'll forgive you. View it as a learning experience. At any rate, it's nice just to see you safe!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                                k.moderator_safe_reply(logger=logger, comment=comment, message=ERROR_UNKNOWN, lock_reply=True)
                                logger.exception('THIS CANNOT CONTINUE.. {}'.format(comment.permalink))
                            else:
                                try:
                                    flairsync.main(comment.parent().author.name)
                                except Exception:
                                    logger.exception('FLAIRSYNC FAILED {}'.format(comment.permalink))
                                SUCCESS_REPLY=f"Cheers for that! /u/{comment.author} you have awarded +karma to user /u/{comment.parent().author.name}!  \n\n ---  \n Don't forget to pop back for another visit, friend. I'll be ready to wheel and deal. Shouldst thee needeth [contact the moderators](https://www.reddit.com/message/compose?to=/r/{subreddit}&subject=About+Patches&message=) of /r/{subreddit}."
                                k.moderator_safe_reply(logger=logger, comment=comment, message=SUCCESS_REPLY, lock_reply=True)
                                if any(word in comment.body.lower() for word in ('close', 'complete', 'thanks', 'gg')) and comment.is_submitter:
                                    post = comment.submission
                                    try:
                                        post.mod.flair(text="Complete!", css_class="duty-fulfilled", flair_template_id="a9bcc130-9a8d-11ec-820c-aa2f5c846ca8")
                                    except:
                                        logger.exception('FAILED TO CLOSE SUBMISSION {}'.format(comment.submission.permalink))
                                # TRIPLE WEEK REPLY, REMOVE AFTER END
                                k.moderator_safe_reply(logger=logger, comment=comment, message=SUCCESS_REPLY, lock_reply=True)
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
                    conversation = subreddit.modmail(modmail.id, mark_read=False)
                    if not k.is_user_older_than_1week(conversation.user):
                        try:
                            conversation.reply(body=f"Hello /u/{conversation.user}! If you are reading this message you have reached out to me Patches to request something silly, unfortunately for you I already told you that new accounts are required to be at least 1 week old to participate in our community, no I will not make an exception!\n Meanwhile please make sure to read the following before try posting again:\n - [Don't be a fool, do not buy runes! (how to dupe runes and items)](https://www.reddit.com/r/PatchesEmporium/comments/1blp0di/dont_be_a_fool_do_not_buy_runes_how_to_dupe_runes/)\n - [FAQ | How to post to r/PatchesEmporium and trade items in Elden Ring](https://www.reddit.com/r/PatchesEmporium/comments/xxjr5u/faq_how_to_post_to_rpatchesemporium_and_trade/) \n\n *** \n I am a bot, and this action was performed automatically.", author_hidden=False)

                            conversation.read(other_conversations=conversation.user.recent_convos)
                            conversation.archive()

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
                                k.sync_karma_to_db(username=info[0],karma=int(info[1]), platform=info[2], subreddit=subreddit.display_name, my_username=my_username)
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
