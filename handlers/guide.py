from aiogram import types
from bot import handler_name


async def class_search(message: types.Message):
    handler_name.set('Class search')
    if len(message.text) < 8:
        await message.reply(
            'Необходимо ввести слова для поиска после /class, орочья ты башка\n'
            'например:\n'
            '/class магический мастеровой\n'
            '/class рывок'
        )
    else:
        spell = ' '.join(message.text.split()[1:])    # remove '/class ' part
        answer = (
            f'Попробуй поискать тут:\n'
            f'[{spell}](https://dnd.su/class/?search={spell})'
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def item_search(message: types.Message):
    handler_name.set('Item search')
    if len(message.text) < 8:
        await message.reply(
            'Это поиск магических предметов, необходимо ввести слова для поиска после /item\n'
            'например:\n'
            '/item жемчужина силы\n'
            '/item посох защиты '
        )
    else:
        spell = ' '.join(message.text.split()[1:])    # remove '/item ' part
        answer = (
            f'Для поиска пройди по ссылке:\n'
            f'[{spell}](https://dnd.su/items/?search={spell})'
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def mech_search(message: types.Message):
    handler_name.set('Mechanic search')
    if len(message.text) < 8:
        await message.reply(
            'Это поиск! чтобы что-то поискать, нужно что-то поискать.\n'
            'необходимо ввести слова для поиска после /mech\n'
            'например:\n'
            '/mech безумие\n'
            '/mech языки'
        )
    else:
        spell = ' '.join(message.text.split()[1:])    # remove '/mech ' part
        answer = (
            f'То что ты ищешь находится здесь:\n'
            f'[{spell}](https://dnd.su/mechanics/?search={spell})'
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
