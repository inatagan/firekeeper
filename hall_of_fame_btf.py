from dotenv import load_dotenv
import os
import praw
from utils import karma as karma_control
from datetime import date
from praw.models import InlineImage




TITLE = "Beyond the fog Hall of Champions {}-{}-{}"


HEADER = """### Welcome to the Hall of Champions {image1}

Spoken echoes of Queen Marika linger here. Shall I share them with you?

>In Marika's own words. My Lord, and thy warriors. I divest each of thee of thy grace. With thine eyes dimmed, ye will be driven from the Lands Between. Ye will wage war in a land afar, where ye will live, and die.
>
>Then, after thy death, I will give back what I once claimed. Return to the Lands Between, wage war, and brandish the Elden Ring.
>
>Grow strong in the face of death. Warriors of my lord. Lord Godfrey.

Greetings, traveler from beyond the fog. Welcome to our hall of Champions, here we gather to celebrate all of those who lay down the golden sign to aid those in need, to those we've a toast to make.

*To your valour, my sword, and our victory together. Long may the Sun shine!!*

*Someone* once said, -we are amidst strange beings, in a strange land.
The flow of time itself is convoluted; with heroes centuries old phasing in and out.

The very fabric wavers, and relations shift and obscure.
There's no telling how much longer your world and mine will remain in contact.

But, use this and lay your golden summon sign down, to summon one another as spirits, cross the gaps between the worlds, and engage in *jolly co-operation*!

### This week Champions
"""


MIDDLE_TEXT = """
### All time Champions
"""


FOOTER = """
Congratulations to all participants of /r/SummonSign and /r/BeyondThefog, if you would like to join the *Hall of Champions* lay down your golden sign, slay every boss, earn your +karma and rise to the ranks.

---
*Art by @[Yuchan](https://www.pixiv.net/en/artworks/97271504)

Farewell foul tarnished, should you need guidance of grace [contact the moderators](https://reddit.com/message/compose?to=/r/BeyondTheFog&subject=About%20the%20Hall%20od%20Champions&message=)

### [About our new karma bot](https://www.reddit.com/r/BeyondTheFog/comments/vrz3gl/traveler_from_beyond_the_fog_let_me_tell_you/)"""


def format_single_table(result_list):
    columns = len(result_list[0]) + 1
    TABLE_HEADER = "-|Tarnished|+karma"
    TABLE_HEADER_2 = '|'.join([':-:'] * columns)
    TABLE_BODY = "\n".join(f"{i}|{row[0]}|{row[1]}"
                for i, row in enumerate(result_list, start=1))
    return f"\n{TABLE_HEADER}\n{TABLE_HEADER_2}\n{TABLE_BODY}\n"


def format_multiple_table(list_psx, list_pc, list_xbox, list_size):
    columns = (len(list_psx[0]))*3 + 1
    TABLE_HEADER = "-|PSX|+karma|PC|+karma|XBOX|+karma"
    TABLE_HEADER_2 = '|'.join([':-:'] * columns)
    TABLE_BODY = "\n".join(f"{i+1}|{list_psx[i][0]}|{list_psx[i][1]}|{list_pc[i][0]}|{list_pc[i][1]}|{list_xbox[i][0]}|{list_xbox[i][1]}"
                for i in range(list_size))
    return f"\n{TABLE_HEADER}\n{TABLE_HEADER_2}\n{TABLE_BODY}\n"


def main():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.environ.get('melina_client_id'),
        client_secret=os.environ.get('melina_client_secret'),
        user_agent=os.environ.get('melina_user_agent'),
        username=os.environ.get('melina_username'),
        password=os.environ.get('melina_password'),
    )
    sub=os.environ.get('melina_subreddit')
    res_week_psx = karma_control.get_weekly_champions_from_subreddit_by_plat(sub, 'ps')
    res_week_pc = karma_control.get_weekly_champions_from_subreddit_by_plat(sub, 'pc')
    res_week_xbox = karma_control.get_weekly_champions_from_subreddit_by_plat(sub, 'xbox')
    try:
        TABLE_WEEK = format_multiple_table(res_week_psx, res_week_pc, res_week_xbox, 15)
    except IndexError as err:
        print(err)
    # TABLE_WEEK = format_single_table(res_week_pc)
    res_all_psx = karma_control.get_all_time_champions_by_plat_coop('ps')
    res_all_pc = karma_control.get_all_time_champions_by_plat_coop('pc')
    res_all_xbox = karma_control.get_all_time_champions_by_plat_coop('xbox')
    # res_all = karma_control.get_all_time_champions()
    # TABLE_All = format_single_table(res_all)
    try:
        TABLE_All = format_multiple_table(res_all_psx, res_all_pc, res_all_xbox, 10)
    except IndexError as err:
        print(err)
    today_date = date.today()
    image = InlineImage(path="assets/banner.jpg", caption="Brave Tarnished... Thy strength befits a crown.")
    media = {"image1": image}
    REPLY_TEXT = f"{HEADER}\n{TABLE_WEEK}\n{MIDDLE_TEXT}\n{TABLE_All}\n{FOOTER}"

    try:
        sub_post = reddit.subreddit(sub).submit(title=TITLE.format(today_date.year, today_date.month, today_date.day), flair_id="b8c3da3c-9345-11ec-9a6c-ee69577ef9a6", inline_media=media,  selftext=REPLY_TEXT, send_replies=False)
        sub_post.mod.distinguish(how="yes")
        sub_post.mod.sticky(state=True)
        sub_post.mod.suggested_sort(sort="confidence")
    except Exception as err:
        print(err)
    

if __name__ == '__main__':
    main()

