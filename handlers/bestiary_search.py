from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fuzzywuzzy import fuzz
from bot import handler_name


async def generate_beast_card_details(card):
    details = {
        'Опасность': card.danger,
        'Альтернатива': card.type
    }

    details_text = '\n'.join([f'{key}: {value}' for key, value in details.items() if value is not None])

    return f'{card.name}\n' \
           f'{details_text}\n' \
           f'[Ссылка на DnD.su](https://dnd.su{card.url})'


async def bestiary_search(message: types.Message):
    handler_name.set('Bestiary search')
    from main import beast_cards
    if len(message.text) < 10:
        await message.reply(
            'Ух ты, память как у золотой рыбки! Тебе нужно ввести слова для поиска после /bestiary.\n'
            'Вот так, например:\n'
            '/bestiary Багбиры\n'
            '/bestiary Вегепигмеи',
            parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True
        )
    else:
        beast = ' '.join(message.text.split()[1:])    # remove '/bestiary ' part
        beast_lower = beast.lower()
        matches = [key for key in beast_cards.keys() if fuzz.partial_ratio(beast_lower, key) > 75]

        if len(matches) == 1:
            card = beast_cards[matches[0]]
            answer = await generate_beast_card_details(card)
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)

        elif 1 < len(matches) < 37:
            beast_inline_kb_full = InlineKeyboardMarkup(row_width=6)
            buttons_list = [InlineKeyboardButton(str(i + 1),
                                                 callback_data=f'beast_{beast_cards[beast].id}')
                            for i, beast in enumerate(matches)]
            beast_inline_kb_full.add(*buttons_list)
            beasts_text = '\n'.join([f'{i + 1}. {beast_cards[beast].name}' for i, beast in enumerate(matches)])
            await message.reply(f'Ой! твой запрос вернул несколько зверюшек:\n{beasts_text}',
                                reply_markup=beast_inline_kb_full)

        else:
            answer = (
                f'Ну что ж, твою зверюшку нужно искать в дебрях бестиария:\n'
                f'[{beast}](https://dnd.su/articles/bestiary/?search={beast})'
            )
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def beast_callback_query(call: types.CallbackQuery):
    from bot import bot
    from main import beast_cards

    if call.data.startswith('beast_'):
        beast_id = call.data[6:]
        card = next((card for card in beast_cards.values() if card.id == beast_id), None)
        if card is not None:
            answer = await generate_beast_card_details(card)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer,
                                        parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
