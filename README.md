# -Firekeeper-
This is an extended reddit user-flair management bot, it keeps track of individual points("+karma") granted by/to users to build reputation. These points are then displayed as user-flair in specific communities.

It was originally made for the community [/r/SummonSign](https://www.reddit.com/r/SummonSign/) with a simpler version and then extended to a more robust bot capable of managing the user-flair system between multiple subreddits including [/r/BeyondTheFog](https://www.reddit.com/r/BeyondTheFog/) and more.


### How to install
Clone this repository to it's destination.

On the root directory of this project run the command to install all the necessary dependencies:

    pip install -r requirements.txt

Use the env_template to set all your info required for the `.env` file.

### [Optional] Create a background service to run the main file with systemd.

    sudo nano /lib/systemd/system/firekeeper.service

On the `extra` directory there is already a template file for the service, if you don't have any custom changes you can just copy the `.service` file to `/lib/systemd/system/` with the command:

    sudo cp ~/firekeeper/extra/systemd_bg_service/firekeeper.service /lib/systemd/system/firekeeper.service

Change the permission of the file to 644:

    sudo chmod 644 /lib/systemd/system/firekeeper.service

Reload the system manager configuration by using the following command:

    sudo systemctl daemon-reload

Start the service using the following command:

    sudo systemctl start firekeeper.service

Stop the service using the following command:

    sudo systemctl stop firekeeper.service

You can enable the service to start at boot as below:

    sudo systemctl enable firekeeper.service

### To run in the background use:
>~~nohup python /firekeeper/karmakeeper.py &~~

Please use and run this bot as a background service with `systemd`.

/home/pi/firekeeper/karmakeeper.py

# Helpful links

https://forums.raspberrypi.com/viewtopic.php?t=202146


https://forums.raspberrypi.com/viewtopic.php?t=72927


https://www.nerdynat.com/programming/2019/run-python-on-your-raspberry-pi-as-background-service/

### Reddit discord feed (EXTRA)
https://danwalker.com/python-discord-reddit-feed/

    