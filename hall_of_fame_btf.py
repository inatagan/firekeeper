from dotenv import load_dotenv
import os
import praw
from utils import karma as karma_control
from datetime import date
from praw.models import InlineImage



image = InlineImage(path="assets/banner.jpg", caption="1")

TITLE = "Beyond the fog Hall of Champions {}-{}-{}"

HEADER = """### Welcome to the Hall of Champions {image1}

Greetings, traveler from beyond the fog. Spoken echoes of Queen Marika linger here. Shall I share them with you?

>In Marika's own words. My Lord, and thy warriors. I divest each of thee of thy grace. With thine eyes dimmed, ye will be driven from the Lands Between. Ye will wage war in a land afar, where ye will live, and die.
>
>Then, after thy death, I will give back what I once claimed. Return to the Lands Between, wage war, and brandish the Elden Ring.
>
>Grow strong in the face of death. Warriors of my lord. Lord Godfrey.

Brave tarnished we are amidst strange beings, in a strange land.
The flow of time itself is convoluted; with heroes centuries old phasing in and out.

The very fabric wavers, and relations shift and obscure.
There's no telling how much longer your world and mine will remain in contact.

But, use this and lay your golden summon sign down, to summon one another as spirits, cross the gaps between the worlds, and engage in *jolly co-operation*!

This week Champions
"""


MIDDLE_TEXT = """
All time Champions
"""

FOOTER = """
---
Congratulations to all participants

[About our new karma bot](https://www.reddit.com/r/BeyondTheFog/comments/vrz3gl/traveler_from_beyond_the_fog_let_me_tell_you/)"""

media = {"image1": image}


def format_table(result_list):
    columns = len(result_list[0]) + 1
    TABLE_HEADER = "-|user|+karma"
    TABLE_HEADER_2 = '|'.join([':-:'] * columns)
    TABLE_BODY = "\n".join(f"{i}|{row[0]}|{row[1]}"
                for i, row in enumerate(result_list, start=1))
    return f"\n{TABLE_HEADER}\n{TABLE_HEADER_2}\n{TABLE_BODY}\n"


def main():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.environ.get('schierke_client_id'),
        client_secret=os.environ.get('schierke_client_secret'),
        user_agent=os.environ.get('schierke_user_agent'),
        username=os.environ.get('schierke_username'),
        password=os.environ.get('schierke_password'),
    )
    sub=os.environ.get('schierke_subreddit')
    res_all = karma_control.get_all_time_champions()
    res_week = karma_control.get_weekly_champions()
    TABLE_WEEK = format_table(res_week)
    TABLE_All = format_table(res_all)
    today_date = date.today()
    REPLY_TEXT = f"{HEADER}\n{TABLE_WEEK}\n{MIDDLE_TEXT}\n{TABLE_All}\n{FOOTER}"

    try:
        sub_post = reddit.subreddit(sub).submit(title=TITLE.format(today_date.year, today_date.month, today_date.day), inline_media=media,  selftext=REPLY_TEXT)
        sub_post.mod.distinguish(how="yes")
        sub_post.mod.sticky(state=2)
    except Exception as err:
        print(err)
    

if __name__ == '__main__':
    main()

