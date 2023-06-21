import psycopg2
import logging


def create_connection():
    try:
        # Connects to the PostgreSQL database within the Docker container
        connection = psycopg2.connect(
            host="db",
            port="5432",
            user="postgres",
            password="postgres",
            database="postgres"
        )
        logging.info("Successfully connected to the database")
        return connection
    except Exception as error:
        logging.error(f"Error connecting to the database: {error}")
        return None


def create_db_tables(connection):
    try:
        cursor = connection.cursor()
        # Create the profiles and messages tables if they don't exist in the db yet
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id BIGINT PRIMARY KEY,
                username VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_messages (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                message TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user_profiles (id)
            );
        """)
        connection.commit()
        cursor.close()
        logging.info("DB tables created successfully")
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error creating DB tables: {error}")
