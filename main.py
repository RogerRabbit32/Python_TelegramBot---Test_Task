import telebot
import logging

from database import create_connection, create_db_tables
from commands import get_random_comic, create_profile, insert_message, get_user_data

# Sets up the bot
bot = telebot.TeleBot("5937207061:AAHHa80kMNeiCDiiVcnMlE5bHGXcFOpw1kw")

# Configures logging format
logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Connects to the database and creates the user profiles
# and messages tables if they don't exist yet
db_connection = create_connection()
if db_connection is not None:
    create_db_tables(db_connection)


@bot.message_handler(commands=['start'])
def send_greeting(message):
    # Sends standard greeting
    greeting = "Hi dear! Welcome to the bot. How can I assist you?"
    bot.send_message(message.chat.id, greeting)


@bot.message_handler(commands=['api'])
def handle_api_command(message):
    # Calls the function to get a random comic from the XKCD API
    comic_data = get_random_comic()

    if comic_data:
        # Retrieves the data we want to send from the API response
        image_url = comic_data['img']
        alt_text = comic_data['alt']
        # Sends the comic image and caption as a reply to the user
        bot.send_photo(message.chat.id, image_url, caption=alt_text)
        # Logs the API request event
        logging.info(
            f"API request triggered by user {message.from_user.id} {message.from_user.username} (success)"
        )
    else:
        bot.reply_to(message, "Sorry, an error occurred while fetching the comic. Please try again later.")
        logging.info(
            f"API request triggered by user {message.from_user.id} {message.from_user.username} (failed)"
        )


@bot.message_handler(commands=['profile'])
def handle_profile_command(message):
    user_messages = get_user_data(db_connection, message.from_user.id)

    if user_messages:
        # Extracts profile ID and username
        _, username, profile_id = user_messages[0]
        messages = "\n".join(message_text for message_text, _, _ in user_messages)  # All user messages
        response = f"Profile ID: {profile_id}\n\nUsername: {username}\n\nMessages:\n{messages}"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "You have no messages yet")


@bot.message_handler(content_types=['text'])
def echo(message):
    # Logs the received message and user info
    logging.info(
        f"User: {message.from_user.id} {message.from_user.username} Received message: {message.text}"
    )
    # Creates user profile in the db if it doesn't exist yet
    create_profile(db_connection, message.from_user.id, message.from_user.username)
    # Stores the message in the DB
    insert_message(db_connection, message.from_user.id, message.text)
    # Echoes the message the user sent
    bot.send_message(message.chat.id, message.text)


# Starts the bot
bot.polling()
