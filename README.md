# -Firekeeper-
This is an extended reddit user-flair management bot, it keeps track of individual points("+karma") granted by/to users to build reputation. These points are then displayed as user-flair in specific communities.

It was originally made for the community [/r/SummonSign](https://www.reddit.com/r/SummonSign/) with a simpler version and then extended to a more robust bot capable of managing the user-flair system between multiple subreddits including [/r/BeyondTheFog](https://www.reddit.com/r/BeyondTheFog/) and more.

### To run in the background use:
>~~nohup python /firekeeper/karmakeeper.py &~~

Please use and run this bot as a background service with `systemd`.

/home/pi/firekeeper/karmakeeper.py

# Helpful links

https://forums.raspberrypi.com/viewtopic.php?t=202146


https://forums.raspberrypi.com/viewtopic.php?t=72927


https://stackoverflow.com/questions/36076867/which-python-script-is-running


https://stackoverflow.com/questions/2975624/how-to-run-a-python-script-in-the-background-even-after-i-logout-ssh


https://www.nerdynat.com/programming/2019/run-python-on-your-raspberry-pi-as-background-service/

### Reddit discord feed (EXTRA)
https://danwalker.com/python-discord-reddit-feed/

### create a service with systemd
    sudo nano /lib/systemd/system/firekeeper.service