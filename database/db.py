import logging
import os
import sqlite3
from contextlib import contextmanager


@contextmanager
def database_connection(commit=False):
    conn = sqlite3.connect('./db/dnd_bot.db')
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    finally:
        conn.close()


def create_if_not_exist():
    db_dir = './db'
    os.makedirs(db_dir, exist_ok=True)

    try:
        with database_connection(commit=True) as cursor:
            # Create table games
            cursor.execute('''CREATE TABLE IF NOT EXISTS games
                         (chat_id INTEGER PRIMARY KEY, game_info TEXT)''')

        with database_connection(commit=True) as cursor:
            # Create table logs
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS logs
                (date text, user_id text, is_private integer, text text)''')
        logging.info('Database created successfully')
    except Exception as e:
        print(f'Error occurred: {e}')
