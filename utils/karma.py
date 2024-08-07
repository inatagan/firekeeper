import re
from database import db_init as db
from sqlite3 import IntegrityError
from prawcore.exceptions import NotFound
import praw.exceptions
import flairsync
import time


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


def get_flair(username, subreddit):
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

def get_karma_from_dict(user_value):
    karma = 0
    karmaCount = re.findall(r'\d+', str(user_value).replace(' ', ''))
    for i in karmaCount:
        karma = int(i)
    return karma


def get_karma_from_db(username):
    connection = db.connect()
    karma = db.get_user_karma(connection, username)
    return int(karma)


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


def sync_flair(reddit, sub, user, user_css='green'):
    reddit.subreddit(sub).flair.set(user[0], text=user[1], css_class=user_css)


def sync_flair_from_db(reddit, sub, user):
    reddit.subreddit(sub).flair.set(user[0], text=user[1], css_class=user[2])


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


def get_platform(submission_title):
    if 'ps3' in str(submission_title).lower():
        return 'ps3'
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
    if 'switch' in str(submission_title).lower():
        return 'switch'


def get_submission_id(comment):
    return comment.link_id


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


def get_user_from_db(username):
    connection = db.connect()
    user_info = []
    try:
        user_karma = db.get_user_karma(connection, username)
        user_info.append(username)
        # user_info.append(str(f'+{user_karma} Karma'))
        user_info.append(user_karma)
        user_info.append(get_css_class(user_karma))
    except Exception as e:
        print(e)
    finally:
        return user_info[:]


def add_karma_to_db(
        from_user, to_user, submission_id, comment_id, 
        submission_title, platform, subreddit):
    connection = db.connect()
    db.create_tables(connection)
    try:
        db.add_karma(connection,from_user, to_user, submission_id, comment_id, submission_title, platform, subreddit)
    except IntegrityError:
        raise
    except Exception:
        raise


def sync_karma_to_db(username, karma, platform, subreddit, my_username='-Firekeeper-'):
    try:
        connection = db.connect()
        db.create_tables(connection)
        for i in range(karma):
            try:
                db.sync_karma_plat(connection, my_username, username, platform, subreddit)
            except IntegrityError:
                raise
            except Exception:
                raise
    except Exception:
        raise
    else:
        flairsync.main(username)


def delete_all_karma_from_user(username):
    try:
        connection = db.connect()
        db.create_tables(connection)
        db.soft_delete_all_karma(connection, username)
    except Exception as err:
        raise
    else:
        flairsync.main(username)


def delete_karma_by_comment_id(comment_id, my_username, reddit):
    comment = reddit.comment(comment_id)
    connection = db.connect()
    db.create_tables(connection)
    try:
        db.delete_by_comment_id(connection, comment_id)
    except Exception:
        raise
    else:
        flairsync.main(comment.parent().author.name)
        comment.downvote()
        comment.refresh()
        comment.replies.replace_more(limit=None)
        for reply in comment.replies.list():
            if reply.author == my_username:
                reply.delete()


def add_non_participant_to_db(username, subreddit):
    connection = db.connect()
    db.create_tables(connection)
    try:
        db.add_non_participant(connection, username, subreddit)
    except IntegrityError:
        raise
    except Exception:
        raise
    else:
        flairsync.main(username)


def remove_non_participant_to_db(username, subreddit):
    connection = db.connect()
    db.create_tables(connection)
    try:
        db.remove_from_non_participant(connection, username, subreddit)
    except IntegrityError:
        raise
    except Exception:
        raise
    else:
        flairsync.main(username)


def is_non_participant(username):
    connection = db.connect()
    db.create_tables(connection)
    return db.is_non_participant(connection, username) > 0


def delete_all_userflair(reddit, sub):
    subreddit = reddit.subreddit(sub)
    deleted = subreddit.flair.delete_all()
    return deleted


def can_change_flair(reddit, sub, username):
    user_info = tuple(reddit.subreddit(sub).flair(redditor=username))
    user_css = user_info[0]['flair_css_class']
    try:
        if any(css_class in user_css for css_class in ('red', 'mod', 'custom')):
            return False
        else:
            return True
    except TypeError:
        return True


def check_command(comment):
    if comment.body.lower().strip().startswith(("+karma", "\\+karma")):
        return True
    return False


def verify_negotiation(user_from, user_to, comment, parent_comment):
    current_comment = comment
    found_from = False
    found_to = False
    post_list = []
    submission_author_name = "-Firekeeper-" if current_comment.submission.author is None else current_comment.submission.author.name
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


def get_all_time_champions():
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_all_time_champions(connection)
    return result_list


def get_all_time_champions_coop():
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_all_time_champions_coop(connection)
    return result_list


def get_all_time_champions_by_plat(platform):
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_all_time_champions_by_plat(connection, platform)
    return result_list


def get_all_time_champions_by_plat_coop(platform):
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_all_time_champions_by_plat_coop(connection, platform)
    return result_list


def get_weekly_champions():
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_weekly_champions(connection)
    return result_list


def get_weekly_champions_by_plat(platform):
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_weekly_champions_by_plat(connection, platform)
    return result_list


def get_weekly_champions_from_subreddit(subreddit):
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_weekly_champions_from_subreddit(connection, subreddit)
    return result_list


def get_weekly_champions_from_subreddit_by_plat(subreddit, platform):
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_weekly_champions_from_subreddit_by_plat(connection, subreddit, platform)
    return result_list


def get_all_time_champions_from_subreddit(subreddit):
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_all_time_champions_from_subreddit(connection, subreddit)
    return result_list


def get_all_time_champions_from_subreddit_by_plat(subreddit, platform):
    connection = db.connect()
    db.create_tables(connection)
    result_list = db.get_all_time_champions_from_subreddit_by_plat(connection, subreddit, platform)
    return result_list


def moderator_safe_reply(logger, comment, message, distinguish_reply=False, sticky_reply=False, lock_reply=False):
    permalink = comment.permalink
    try:
        bot_reply = comment.reply(body=message)
        logger.debug('REPLY SUCCESS: {}'.format(permalink))
    except praw.exceptions.RedditAPIException:
        logger.exception('REPLY FAIL: {}'.format(permalink))
        return False
    else:
        if sticky_reply:
            bot_reply.mod.distinguish(sticky=True)
        elif distinguish_reply:
            bot_reply.mod.distinguish(how="yes")
        if lock_reply:
            bot_reply.mod.lock()
    logger.debug('REPLIED TO: {}'.format(permalink))
    return True


def submission_clear(submission, my_username, logger):
    connection = db.connect()
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        if comment.author == my_username:
            comment_karma = comment.parent()
            try:
                db.delete_by_comment_id(connection, comment_karma.id)
            except Exception:
                logger.exception('DELETION FAIL: {}'.format(comment.permalink))
            else:
                flairsync.main(comment_karma.parent().author.name)
                comment.delete()

def is_user_older_than_1week(user):
    redditor=user
    created_at=redditor.created_utc
    now=time.time()
    if now - created_at > 604800:
        return True