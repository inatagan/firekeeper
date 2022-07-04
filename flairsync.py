from dotenv import load_dotenv
import os
import praw
from utils import karma


load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ.get('flairsync_client_id'),
    client_secret=os.environ.get('flairsync_client_secret'),
    user_agent=os.environ.get('flairsync_user_agent'),
    username=os.environ.get('flairsync_username'),
    password=os.environ.get('flairsync_password'),
)


def main(username):
    try:
        user_karma = karma.getKarmaFromDB(username)
        user_css =  karma.getCSSClass(user_karma)
    except Exception as err:
        return err
    else:
        sub_list = ('SummonSign', 'BeyondTheFog')
        for sub in sub_list:
            if karma.can_change_flair(reddit, sub, username):
                if user_karma > 1000:
                    if 'SummonSign' in sub:
                        new_flair_text = str(f'+{user_karma} k | Lord of Hollows')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                    elif 'BeyondTheFog' in sub:
                        new_flair_text = str(f'+{user_karma} k | Dark Moon Lord')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                elif user_karma > 500:
                    if 'SummonSign' in sub:
                        new_flair_text = str(f'+{user_karma} k | Grossly Incandescent')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                    elif 'BeyondTheFog' in sub:
                        new_flair_text = str(f'+{user_karma} k | Lord of Frenzied Flame')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                elif user_karma > 250:
                    if 'SummonSign' in sub:
                        new_flair_text = str(f'+{user_karma} k | Warrior of Sunlight')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                    elif 'BeyondTheFog' in sub:
                        new_flair_text = str(f'+{user_karma} k | Furled Finger')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                elif user_karma > 100:
                    if 'SummonSign' in sub:
                        new_flair_text = str(f'+{user_karma} k | Warrior of Sunlight')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                    elif 'BeyondTheFog' in sub:
                        new_flair_text = str(f'+{user_karma} k | Furled Finger')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                elif user_karma > 50:
                    if 'SummonSign' in sub:
                        new_flair_text = str(f'+{user_karma} k | Warrior of Sunlight')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                    elif 'BeyondTheFog' in sub:
                        new_flair_text = str(f'+{user_karma} k | Furled Finger')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                elif user_karma > 15:
                    if 'SummonSign' in sub:
                        new_flair_text = str(f'+{user_karma} k | Ash')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                    elif 'BeyondTheFog' in sub:
                        new_flair_text = str(f'+{user_karma} k | Foul Tarnished')
                        try:
                            reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                        except:
                            pass
                else:
                    new_flair_text = str(f'+{user_karma} Karma')
                    try:
                        reddit.subreddit(sub).flair.set(username, text=new_flair_text, css_class=user_css)
                    except:
                        pass




if __name__ == '__main__':
    main()

