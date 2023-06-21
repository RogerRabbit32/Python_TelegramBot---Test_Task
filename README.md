# Python_TelegramBot---Test_Task
This project represents a simple Telegram echo bot with a couple of additional features.

The standard bot behavior is simply replying to any text messages from the user with the same
message text, any other content (e.g. photos, videos) is ignored. However, some commands implement
additional features.

The available bot commands are:

<b>/start</b> - Replies to the user with a standard greeting<br/>
<b>/api</b> - Sends request to an external API (https://xkcd.com/), fetches a random comic
        and replies to the user with its picture and a caption to it<br/>
<b>/profile</b> - Retrieves the user profile data from the app database, replies to the user
        with their ID and username in the system (saved as Telegram ID and username)
        and the message history with the bot, stored in the database

To launch the project, run the command

<code>docker-compose up</code>

The project utilizes Docker volumes, so there should be no DB data losses.
