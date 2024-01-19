from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def character_creation_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton('Пресет', callback_data='toggle_list'),
        InlineKeyboardButton('Класс', callback_data='select_class'),
        InlineKeyboardButton('Раса', callback_data='select_race'),
        InlineKeyboardButton('Предыстория', callback_data='select_story'),
        InlineKeyboardButton('Количество', callback_data='select_num_chars'),
        InlineKeyboardButton('Сбросить', callback_data='reset_char'),
        InlineKeyboardButton('Создать', callback_data='generate'),
    )
    return keyboard
