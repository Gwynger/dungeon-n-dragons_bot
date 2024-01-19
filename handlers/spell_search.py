from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fuzzywuzzy import fuzz
from bot import handler_name


async def generate_spell_card_details(card):
    details = {
        'Время накладывания': card.casting_time,
        'Дистанция': card.c_range,
        'Компоненты': card.components,
        'Длительность': card.duration,
        'Классы': card.classes,
        'Архетипы': card.archetypes,
    }

    details_text = '\n'.join([f'{key}: {value}' for key, value in details.items() if value is not None])

    return f'{card.title} [[{card.title_en}]]\n\n' \
           f'{card.level_school}\n' \
           f'{details_text}\n\n' \
           f'{card.description}\n\n' \
           f'[Ссылка на DnD.su](https://dnd.su{card.link})'


async def spell_search(message: types.Message):
    handler_name.set('Spell search')
    from main import spell_cards
    if len(message.text) < 8:
        await message.reply(
            'Ты забыл ввести слова для поиска после /spell\n'
            'например:\n'
            '/spell водоворот\n'
            '/spell Власть над водами'
        )
    else:
        spell = ' '.join(message.text.split()[1:])  # remove '/spell ' part
        spell_lower = spell.lower()
        # Use fuzzy matching for better results
        matches = [card.id for card in spell_cards.values() if fuzz.partial_ratio(spell_lower, card.title.lower()) > 75]

        if len(matches) == 1:
            card = spell_cards[matches[0]]
            answer = await generate_spell_card_details(card)
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)

        elif 1 < len(matches) < 25:
            spell_inline_kb_full = InlineKeyboardMarkup(row_width=6)
            buttons_list = [InlineKeyboardButton(str(i + 1),
                                                 callback_data=f'spell_{spell_cards[spell].id}') for i, spell in
                            enumerate(matches)]
            spell_inline_kb_full.add(*buttons_list)
            spells_text = '\n'.join([f'{i + 1}. {spell_cards[spell].title}'
                                     f' [{spell_cards[spell].title_en}]' for i, spell in enumerate(matches)])
            await message.reply(f'В базе несколько заклинаний по вашему запросу:\n{spells_text}',
                                reply_markup=spell_inline_kb_full)

        else:
            answer = (
                'твоё заклинание где-то здесь:\n'
                f'[{spell}](https://dnd.su/spells/?search={spell})'
            )
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def spell_callback_query(call: types.CallbackQuery):
    from bot import bot
    from main import spell_cards

    if call.data.startswith('spell_'):
        spell_id = int(call.data[6:])  # Parse the spell id
        card = spell_cards[spell_id]
        answer = await generate_spell_card_details(card)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer,
                                    parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
