from dotenv import load_dotenv
import os
import praw
from utils import karma as karma_control
from datetime import date




TITLE = "Beyond the fog Hall of Champions {}-{}-{}"

TEXT = """### Welcome to the Hall of Champions
Greetings, traveller from beyond the fog. Spoken echoes of Queen Marika linger here. Shall I share them with you?

>In Marika's own words. My Lord, and thy warriors. I divest each of thee of thy grace. With thine eyes dimmed, ye will be driven from the Lands Between. Ye will wage war in a land afar, where ye will live, and die.
>
>Then, after thy death, I will give back what I once claimed. Return to the Lands Between, wage war, and brandish the Elden Ring.
>
>Grow strong in the face of death. Warriors of my lord. Lord Godfrey.

This week Champions

-|user|karma
:-:|:-:|:-:
1|{}|{}
2|{}|{}
3|{}|{}
4|{}|{}
5|{}|{}
6|{}|{}
7|{}|{}
8|{}|{}
9|{}|{}
10|{}|{}


All time Champions

-|user|karma
:-:|:-:|:-:
1|{}|{}
2|{}|{}
3|{}|{}
4|{}|{}
5|{}|{}
6|{}|{}
7|{}|{}
8|{}|{}
9|{}|{}
10|{}|{}

---
[About our new karma bot](https://www.reddit.com/r/BeyondTheFog/comments/vrz3gl/traveler_from_beyond_the_fog_let_me_tell_you/)"""

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
    today_date = date.today()

    sub_post = reddit.subreddit(sub).submit(title=TITLE.format(today_date.year, today_date.month, today_date.day),  selftext=TEXT.format(res_week[0][0], res_week[0][1], res_week[1][0], res_week[1][1], res_week[2][0], res_week[2][1], res_week[3][0], res_week[3][1], res_week[4][0], res_week[4][1], res_week[5][0], res_week[5][1], res_week[6][0], res_week[6][1], res_week[7][0], res_week[7][1], res_week[8][0], res_week[8][1], res_week[9][0], res_week[9][1], res_all[0][0], res_all[0][1], res_all[1][0], res_all[1][1], res_all[2][0], res_all[2][1], res_all[3][0], res_all[3][1], res_all[4][0], res_all[4][1], res_all[5][0], res_all[5][1], res_all[6][0], res_all[6][1], res_all[7][0], res_all[7][1], res_all[8][0], res_all[8][1], res_all[9][0], res_all[9][1]))
    sub_post.mod.distinguish(how="yes")
    sub_post.mod.sticky(state=2)


if __name__ == '__main__':
    main()

