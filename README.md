# -Firekeeper-
This is an extended reddit user-flair management bot, it keeps track of individual points("+karma") granted by/to users to build reputation. These points are then displayed as user-flair in specific communities.

It was originally made for the community [/r/SummonSign](https://www.reddit.com/r/SummonSign/) with a simpler version and then extended to a more robust bot capable of managing the user-flair system between multiple subreddits including [/r/BeyondTheFog](https://www.reddit.com/r/BeyondTheFog/) and more.


### How to install
Clone this repository to it's destination.

Create a Python Virtual Environment:

    python3 -m venv venv

Activate the Virtual Environment:

    source venv/bin/activate

On the root directory of this project run the command to install all the necessary dependencies:

    pip install -r requirements.txt

Use the env_template to set all your info required for the `.env` file.

### [Optional] Create a background service to run the main file with systemd.

    sudo nano /lib/systemd/system/firekeeper.service

On the `extra` directory there is already a template file for the service, if you don't have any custom changes you can just copy the `.service` file to `/lib/systemd/system/` with the command:

    # this template is already set to run with the VENV just replace the $USER with your user.
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

### How to use

#### The +karma command
The main feature of this bot is to monitor a subreddit, this bot will scan through all the comments looking for this command, to trigger the comment reply must start with the command `+karma`, then this bot will do all the checks and reply appropriately.

#### The mod log
This bot also will keep track of moderator actions and in the event of a removal of thread where +karma was given, on the event of the removal the bot will scan the thread to see if any +karma was given and if it was it will automatically reverse it back. Besides the checks already implemented it is also understood that this bot will not reward rule breaking submissions.

#### Moderator's commands
To help better manage the +karma system now there is several helpful commands through private messages available to moderators. Be aware that to be able to use these commands the moderator must have permission to send private messages to this bot's account.

These commands are quite simple to use, when sending a private message to the bot use the subject field to add a command and then use the body of the message to add any data necessary.

    add non participant

Subject input: `add non participant`.

Body input: `username`

This will add a user to the non participants list, this is a list of users that can use the subreddit without being part of the karma system, for those who desire and also banned users are automatically added to this list.

    remove non participant

Subject input: `remove non participant`

Body input: `username`

This will remove a user of the non participants list.

    thread clear

Subject input: `thread clear`

Body input: `URL`

This will clear all the karma given in a submission, the `URL` must be the permalink to the thread, it also works on threads that are deleted by the original poster.

    sync karma

Subject input: `sync karma`

Body input: `username`, `karma`, `platform`

This will add one or many karma to a user. The body input must be in the described other separated by commas `,`.

    delete all karma

Subject input: `delete all karma`

Body input: `username`

This will delete all karma of a user.

    delete karma by comment

Subject input: `delete karma by comment`

Body input: `comment permalink`

This will delete one particular karma from a comment.


# Helpful links

https://forums.raspberrypi.com/viewtopic.php?t=202146


https://forums.raspberrypi.com/viewtopic.php?t=72927


https://www.nerdynat.com/programming/2019/run-python-on-your-raspberry-pi-as-background-service/

### Reddit discord feed (EXTRA)
https://danwalker.com/python-discord-reddit-feed/

    