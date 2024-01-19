from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import bot, handler_name
from keyboards.keyboard import character_creation_keyboard
from utils.character_creation_utils import (
    generate_current_settings_message,
    make_character,
    reset_user_settings,
    user_choices,
)
from utils.masterdata import (
    CLASSES,
    CLASSIC_CLASSES,
    CLASSIC_RACES,
    CLASSIC_STORIES,
    RACES,
    STORIES,
)


async def create_character(message: types.Message):
    handler_name.set('Create character')
    reset_user_settings(message.chat.id)
    answer = generate_current_settings_message(message.chat.id)
    await bot.send_message(
        message.chat.id,
        answer,
        reply_markup=character_creation_keyboard()
    )


# add the reset functionality to the callback handler for 'reset_char' button
async def reset_char_settings(callback_query: types.CallbackQuery):
    reset_user_settings(callback_query.from_user.id)  # Reset user settings
    answer = generate_current_settings_message(callback_query.from_user.id)  # Generate settings message after reset
    await bot.answer_callback_query(callback_query.id)
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=answer,
            reply_markup=character_creation_keyboard()
        )
    except Exception as e:
        # Обработка других исключений, если они возникают
        print(f"An error occurred while editing the message: {e}")


# Handler for 'Пресет' button
async def toggle_list(callback_query: types.CallbackQuery):
    # Get current choice
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    # Toggle preset
    preset = 'Расширенный' if preset == 'Классика' else 'Классика'
    user_choice['preset'] = preset
    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard())


# Handler for 'Класс' button
async def select_class(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    classes = CLASSIC_CLASSES if preset == 'Классика' else CLASSES
    keyboard = InlineKeyboardMarkup(row_width=3)
    for class_name in classes:
        button = InlineKeyboardButton(class_name, callback_data=f'selected_class_{class_name}')
        keyboard.insert(button)

    await bot.edit_message_text(
        'Выберите класс:',
        chat_id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )


# Handler for when a class is selected
async def selected_class(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    class_name = callback_query.data[len('selected_class_'):]

    # Update user choice
    user_choice['char_class'] = class_name

    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard()
    )


# Handler for 'раса' button
async def select_race(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    races = CLASSIC_RACES if preset == 'Классика' else RACES
    keyboard = InlineKeyboardMarkup(row_width=3)
    for race_name in races:
        button = InlineKeyboardButton(race_name, callback_data=f'selected_race_{race_name}')
        keyboard.insert(button)

    await bot.edit_message_text(
        'Выберите расу:',
        chat_id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )


# Handler for when a race is selected
async def select_race_choice(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    race_name = callback_query.data[len('selected_race_'):]

    # Update user choice
    user_choice['char_race'] = race_name

    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard()
    )


# Handler for 'История' button
async def select_story(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    stories = CLASSIC_STORIES if preset == 'Классика' else STORIES
    keyboard = InlineKeyboardMarkup(row_width=3)
    for story_name in stories:
        button = InlineKeyboardButton(story_name, callback_data=f'selected_story_{story_name}')
        keyboard.insert(button)

    await bot.edit_message_text(
        'Выберите предысторию:',
        chat_id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )


# Handler for when a story is selected
async def select_story_choice(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    story_name = callback_query.data[len('selected_story_'):]

    # Update user choice
    user_choice['char_story'] = story_name

    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard()
    )


# Handler for 'Количество персонажей' button
async def select_num_chars(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Create keyboard for selecting number of characters
    keyboard = InlineKeyboardMarkup(row_width=5)
    for i in range(1, 11):
        button = InlineKeyboardButton(str(i), callback_data=f'selected_num_chars_{i}')
        keyboard.insert(button)

    await bot.edit_message_text(
        'Выберите количество персонажей:',
        chat_id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )


# Handler for when a number of characters is selected
async def selected_num_chars(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    num_chars = int(callback_query.data[len('selected_num_chars_'):])

    # Update user choice
    user_choice['num_chars'] = num_chars

    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard()
    )


# Handler for 'Создать' button
async def generate(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.get(chat_id, {})
    # Get choices
    preset = user_choice.get('preset', 'Классика')
    char_class = user_choice.get('char_class', 'Случайно')
    race = user_choice.get('char_race', 'Случайно')
    story = user_choice.get('char_story', 'Случайно')
    num_chars = user_choice.get('num_chars', 3)
    # Generate characters
    characters = '\n---\n'.join(make_character(char_class, race, story, preset == 'Классика') for _ in range(num_chars))
    # Send characters
    await bot.send_message(chat_id, characters, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
