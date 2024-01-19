import logging
from contextvars import ContextVar
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from dotenv import dotenv_values

ENV = dotenv_values('.env')
API_TOKEN = ENV['TOKEN']   # your telegram bot token

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

handler_name = ContextVar('handler_name', default='')


class LoggingMiddleware(BaseMiddleware):
    async def on_post_process_message(self, message: types.Message, *args):
        from database.utils import log_message
        log_message(message)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.setup_middleware(LoggingMiddleware())
