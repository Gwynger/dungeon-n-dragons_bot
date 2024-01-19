import logging
from dotenv import dotenv_values
import handlers.bestiary_search
from bot import dp
from database.db import create_if_not_exist
from handlers import (
    create_char,
    feat_search,
    guide,
    next_game,
    roll,
    spell_search,
    start,
)
from handlers.statistics import on_csv_button, stats_command
from utils.masterdata import load_beasts, load_feats, load_spells
from aiogram import types

ENV = dotenv_values('.env')
ADMIN_ID = ENV['ADMIN_ID']

create_if_not_exist()
spell_cards = load_spells('utils/spells.json')
feat_cards = load_feats('utils/feats.json')
beast_cards = load_beasts('utils/beasts.json')
logging.info('Spells, feats and beasts loaded')


def register_handlers_for_dp(dp):
    dp.register_message_handler(start.start_message, commands=['start'])
    dp.register_message_handler(start.help_message, commands=['help'])
    dp.register_message_handler(next_game.set_game, commands=['set'])
    dp.register_message_handler(next_game.get_game, commands=['game'])
    dp.register_message_handler(guide.class_search, commands=['class'])
    dp.register_message_handler(guide.mech_search, commands=['mech'])
    dp.register_message_handler(guide.item_search, commands=['item'])
    dp.register_message_handler(create_char.create_character, commands=['create_character'])

    dp.register_message_handler(handlers.bestiary_search.bestiary_search, commands=['bestiary'])
    dp.register_callback_query_handler(handlers.bestiary_search.beast_callback_query,
                                       lambda call: call.data.startswith('beast_'))

    dp.register_message_handler(spell_search.spell_search, commands=['spell'])
    dp.register_callback_query_handler(spell_search.spell_callback_query, lambda call: call.data.startswith('spell_'))

    dp.register_message_handler(feat_search.feat_search, commands=['feat'])
    dp.register_callback_query_handler(feat_search.feat_callback_query, lambda call: call.data.startswith('feat_'))

    # create_char
    dp.register_callback_query_handler(create_char.reset_char_settings, lambda c: c.data == 'reset_char')
    dp.register_callback_query_handler(create_char.toggle_list, lambda c: c.data == 'toggle_list')
    dp.register_callback_query_handler(create_char.select_class, lambda c: c.data == 'select_class')
    dp.register_callback_query_handler(create_char.selected_class, lambda c: c.data.startswith('selected_class_'))
    dp.register_callback_query_handler(create_char.select_race, lambda c: c.data == 'select_race')
    dp.register_callback_query_handler(create_char.select_race_choice,
                                       lambda c: c.data and c.data.startswith('selected_race_'))
    dp.register_callback_query_handler(create_char.select_story, lambda c: c.data == 'select_story')
    dp.register_callback_query_handler(create_char.select_story_choice,
                                       lambda c: c.data and c.data.startswith('selected_story_'))
    dp.register_callback_query_handler(create_char.select_num_chars, lambda c: c.data == 'select_num_chars')
    dp.register_callback_query_handler(create_char.selected_num_chars,
                                       lambda c: c.data.startswith('selected_num_chars_'))
    dp.register_callback_query_handler(create_char.generate, lambda c: c.data == 'generate')

    dp.register_message_handler(stats_command, commands=['stats'], user_id=ADMIN_ID)
    dp.register_callback_query_handler(on_csv_button)

    dp.register_message_handler(roll.roll_dice_command, commands=['roll'])
    dp.register_message_handler(roll.dice_roll)  # should be the last one, because it has a catch-all handler


if __name__ == '__main__':
    register_handlers_for_dp(dp)
    dp.start_polling(skip_updates=False)
