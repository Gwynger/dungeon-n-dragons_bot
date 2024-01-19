from aiogram import types
from bot import handler_name
from database.utils import db_get_game, db_set_game


async def set_game(message: types.Message):
    handler_name.set('Set game')
    chat_id = message.chat.id
    game_info = message.text[5:]  # Removes the '/set ' part
    db_set_game(chat_id, game_info)

    await message.reply('Информация о следующей партии сохранена')


async def get_game(message: types.Message):
    handler_name.set('Get game')
    chat_id = message.chat.id
    game_info = db_get_game(chat_id)

    if game_info is None:
        await message.reply('Информации о следующей игре нет. может быть вы забыли о команде /set?')
    else:
        await message.reply(game_info[0])
