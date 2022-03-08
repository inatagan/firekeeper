# reddit-feed.py - posts new subreddit posts to a Discord channel via webhook
# author:  Dan Walker
# email:   code@danwalker.com
# url:     https://danwalker.netlify.app/python-discord-reddit-feed/
# created: 2020-08-13  

import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os

# open the cache, or start from a blank list
try:
    with open('btf_db.json') as json_file:
        btf_db = json.load(json_file)
except FileNotFoundError:
    btf_db = []

#load .end
load_dotenv()

webhook_url = os.environ.get('my_webhook_2')
subreddit   = os.environ.get('subreddit_2') # can be chained with + (example: python+webdev)

req = requests.get(f'https://www.reddit.com/r/{subreddit}/new/.json', headers={
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "User-Agent": "discord-feed-bot"})

posts = req.json()['data']['children']

# for each new post found in this request
for post in posts:
    if post['data']['name'] not in btf_db:
        webhook = DiscordWebhook(url=webhook_url)
        permalink = f"https://www.reddit.com{post['data']['permalink']}"

        # create an appropriate embed object
        if post['data']['thumbnail'] == 'self': # text post
            embed = DiscordEmbed(title=post['data']['title'], url=permalink, description=post['data']['selftext'])
            embed.set_footer(text=f"Posted by {post['data']['author']}")
        elif post['data']['is_video']: # video post
            embed = DiscordEmbed(title=post['data']['title'], url=permalink)
            embed.set_image(url=post['data']['thumbnail'])
            embed.set_footer(text=f"Video posted by {post['data']['author']}")
        else: # image post
            embed = DiscordEmbed(title=post['data']['title'], url=permalink)
            embed.set_image(url=post['data']['url'])
            embed.set_footer(text=f"Image posted by {post['data']['author']}")

        # attach the embed to the webhook request and go!
        webhook.add_embed(embed)
        webhook.execute()
        time.sleep(1) # to prevent Discord webhook rate limiting

        # add post name to btf_DB so we don't display it again
        btf_db.append(post['data']['name'])

# save the cache of (at least) the last 50 posts seen
with open('btf_db.json', 'w') as outfile:
    json.dump(btf_db[-50:], outfile)

