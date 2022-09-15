from dotenv import load_dotenv
import os
import praw
from utils import karma as karma_control
from datetime import date
from praw.models import InlineImage




TITLE = "Summon Sign Hall of Champions {}-{}-{}"


HEADER = """### Welcome to the Hall of Champions {image1}

>The five lords sit their five thrones. All thanks to thee, most worthy of lords. Ashen one, with the Lords as thy witness, bend thy knee afore the bonfire's coiled sword. And let the Lords' embers acknowledge thee as their true heir. A true lord, fit to link the fire.
>
>Noble Lords of Cinder. The fire fades... and the lords go without thrones. Surrender your fires... to the true heir. Let him grant death... To the old gods of Lordran, deliverers of the First Flame.
>
>Ashen one, link the fire. For the Lords of Cinder, for the ashen prisoners, for all those held to preserve the fire. Link the First Flame!

Welcome to our *Hall of Champions*, Unkindled One. here we gather to celebrate all of those who lay down the golden sign to aid those in need, to those we've a toast to make.

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
Congratulations to all participants of /r/SummonSign and /r/BeyondThefog, if you would like to join the *Hall of Champions* lay down your golden sign, slay every soul, earn your +karma and rise to the ranks.

---
*Art by @[S-Mrry](https://www.pixiv.net/en/artworks/92892358)

Farewell chosen undead, should your heart bend [contact the moderators](https://reddit.com/message/compose?to=/r/SummonSign&subject=About%20the%20Hall%20od%20Champions&message=)

### [About our new karma bot](https://www.reddit.com/r/SummonSign/comments/vs01fk/ashen_one_let_me_tell_you_about_the_new_karma_bot/)"""


def format_table(result_list):
    columns = len(result_list[0]) + 1
    TABLE_HEADER = "-|Ashen one|+karma"
    TABLE_HEADER_2 = '|'.join([':-:'] * columns)
    TABLE_BODY = "\n".join(f"{i}|{row[0]}|{row[1]}"
                for i, row in enumerate(result_list, start=1))
    return f"\n{TABLE_HEADER}\n{TABLE_HEADER_2}\n{TABLE_BODY}\n"


def main():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.environ.get('my_client_id'),
        client_secret=os.environ.get('my_client_secret'),
        user_agent=os.environ.get('my_user_agent'),
        username=os.environ.get('my_username'),
        password=os.environ.get('my_password'),
    )
    sub=os.environ.get('my_subreddit')
    res_week = karma_control.get_weekly_champions_from_subreddit(sub)
    TABLE_WEEK = format_table(res_week)
    res_all = karma_control.get_all_time_champions()
    TABLE_All = format_table(res_all)
    today_date = date.today()
    image = InlineImage(path="assets/hof_summonsign_banner.png", caption="The fire fades... plin, plin, plon..")
    media = {"image1": image}
    REPLY_TEXT = f"{HEADER}\n{TABLE_WEEK}\n{MIDDLE_TEXT}\n{TABLE_All}\n{FOOTER}"

    try:
        sub_post = reddit.subreddit(sub).submit(title=TITLE.format(today_date.year, today_date.month, today_date.day), flair_id="b847e3d0-5469-11eb-adff-0e82fa5aa449", inline_media=media,  selftext=REPLY_TEXT, send_replies=False)
        sub_post.mod.distinguish(how="yes")
        sub_post.mod.sticky(state=True)
        sub_post.mod.suggested_sort(sort="confidence")
    except Exception as err:
        print(err)
    

if __name__ == '__main__':
    main()

