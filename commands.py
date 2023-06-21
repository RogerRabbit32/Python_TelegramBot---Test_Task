import random
import requests
import logging
import psycopg2


# Defines making requests to the XKCD API to fetch a random comic
def get_random_comic():
    random_comic_id = random.randint(1, 2790)
    url = f"https://xkcd.com/{random_comic_id}/info.0.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Defines creating user profile (if doesn't exist yet)
def create_profile(db_connection, user_id, username):
    try:
        cursor = db_connection.cursor()

        # Check if a user with this ID already exists
        cursor.execute(
            "SELECT * FROM user_profiles WHERE id = %s", (user_id,)
        )
        user = cursor.fetchone()

        if not user:
            # If user doesn't exist, insert a new profile and log successful creation
            cursor.execute(
                "INSERT INTO user_profiles (id, username) VALUES (%s, %s)", (user_id, username)
            )
            logging.info(
                f"Successfully created new user profile {user_id} {username}"
            )

        db_connection.commit()
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error inserting new user {user_id} {username} profile: {error}")


# Defines storing user messages in the DB
def insert_message(db_connection, user_id, message_text):
    try:
        cursor = db_connection.cursor()

        # Insert the new message into the user_messages table
        cursor.execute("INSERT INTO user_messages (user_id, message) VALUES (%s, %s)",
                       (user_id, message_text))

        db_connection.commit()
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error inserting message: {error}")


# Defines retrieving user messages from the DB
def get_user_data(db_connection, user_id):
    try:
        cursor = db_connection.cursor()

        # Retrieve user messages along with the username from the database
        cursor.execute("""
            SELECT m.message, p.username, p.id
            FROM user_messages AS m
            JOIN user_profiles AS p ON m.user_id = p.id
            WHERE p.id = %s
        """, (user_id,))

        message_data = cursor.fetchall()

        cursor.close()
        return message_data
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error retrieving user messages with username: {error}")
        return None
