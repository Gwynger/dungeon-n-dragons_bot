import logging
from datetime import datetime, timedelta
from aiogram import types
from database.db import database_connection


def log_message(message: types.Message):
    from bot import handler_name
    handler = handler_name.get()
    if handler != '' and handler != 'Stats':
        with database_connection(commit=True) as cursor:
            is_private = 1 if message.chat.id > 0 else 0

            cursor.execute('INSERT INTO logs VALUES (?, ?, ?, ?)', (str(datetime.now()), message.from_user.id,
                                                                    int(is_private), handler))
            logging.debug(f'Message logged: {message.text}, handler: {handler}')


def get_week_stats():
    with database_connection() as cursor:
        week_ago = datetime.now() - timedelta(days=7)
        query = f"""
        SELECT COUNT(DISTINCT user_id), COUNT(*)
        FROM logs
        WHERE date > '{week_ago.strftime('%Y-%m-%d %H:%M:%S')}'
        """
        cursor.execute(query)
        result = cursor.fetchone()

    return result


def get_month_stats():
    with database_connection() as cursor:

        month_ago = datetime.now() - timedelta(days=30)
        query = f"""
        SELECT COUNT(DISTINCT user_id), COUNT(*)
        FROM logs
        WHERE date > '{month_ago.strftime('%Y-%m-%d %H:%M:%S')}'
        """
        cursor.execute(query)
        result = cursor.fetchone()

    return result


def get_top_5_requests():
    with database_connection() as cursor:
        week_ago = datetime.now() - timedelta(days=7)
        query = f"""
        SELECT text, COUNT(*)
        FROM logs
        WHERE date > '{week_ago.strftime('%Y-%m-%d %H:%M:%S')}'
        GROUP BY text
        ORDER BY COUNT(*) DESC
        LIMIT 5
        """
        cursor.execute(query)
        result = cursor.fetchall()

    return result


def db_set_game(chat_id: str, game_info: str):
    with database_connection(commit=True) as cursor:
        cursor.execute('''INSERT OR REPLACE INTO games (chat_id, game_info)
                     VALUES (?, ?)''', (chat_id, game_info))


def db_get_game(chat_id: int):
    with database_connection(commit=True) as cursor:
        cursor.execute('SELECT game_info FROM games WHERE chat_id = ?', (chat_id,))
        game_info = cursor.fetchone()
    return game_info
