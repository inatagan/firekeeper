from dotenv import load_dotenv
import os
import praw

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
    userflair_list = subreddit.flair.delete_all()


    for flair in userflair_list:
        # Use the command bellow to create an quick and dirty flair list for reference:
        # unbuffer python3 flairdump_and_delete_all.py 2>&1 | tee -a sub_flair_list.log
        # user_info = (flair['user'].name, flair['flair_text'])
        print(flair)



if __name__ == '__main__':
    main()