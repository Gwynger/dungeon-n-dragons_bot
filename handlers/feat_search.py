from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fuzzywuzzy import fuzz
from bot import handler_name


async def generate_feat_card_details(card):
    details = {
        'Требования': card.requirements,
        'Полное описание': card.description,
    }

    details_text = '\n'.join([f'{key}: {value}' for key, value in details.items() if value is not None])

    return f'{card.title} [[{card.title_en}]]\n\n' \
           f'{details_text}\n\n' \
           f'[Ссылка на DnD.su](https://dnd.su{card.link})'


async def feat_search(message: types.Message):
    handler_name.set('Feat search')
    from main import feat_cards
    if len(message.text) < 6:
        await message.reply(
            'Ты забыл ввести слова для поиска после /feat\n'
            'например:\n'
            '/feat Борец\n'
            '/feat Инфернальное телосложение'
        )
    else:
        feat = ' '.join(message.text.split()[1:])    # remove '/feat ' part
        feat_lower = feat.lower()
        matches = [card.id for card in feat_cards.values() if fuzz.partial_ratio(feat_lower, card.title.lower()) > 75]
        if len(matches) == 1:
            card = feat_cards[matches[0]]
            answer = await generate_feat_card_details(card)
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)

        elif 1 < len(matches) < 37:
            feat_inline_kb_full = InlineKeyboardMarkup(row_width=6)
            buttons_list = [InlineKeyboardButton(str(i + 1),
                                                 callback_data=f'feat_{feat_cards[feat].id}') for i, feat
                            in enumerate(matches)]
            feat_inline_kb_full.add(*buttons_list)
            feats_text = '\n'.join([f'{i+1}. {feat_cards[feat].title}'
                                    f' [{feat_cards[feat].title_en}]' for i, feat in enumerate(matches)])
            await message.reply(f'В базе несколько черт по вашему запросу:\n{feats_text}',
                                reply_markup=feat_inline_kb_full)

        else:
            answer = (
                'черта где-то здесь:\n'
                f'[{feat}](https://dnd.su/feats/?search={feat})'
            )
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def feat_callback_query(call: types.CallbackQuery):
    from bot import bot
    from main import feat_cards
    if call.data.startswith('feat_'):
        feat_id = int(call.data[5:])
        card = feat_cards[feat_id]
        answer = await generate_feat_card_details(card)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer,
                                    parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
