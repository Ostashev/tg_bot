import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from src.database.engine import AsyncSessionLocal
from src.handlers import commands, callbacks
from src.handlers.base import start_handler
from config import config
from src.handlers import create_mail_message_router
from src.middleware.datebase import DataBaseSession
from src.states.base import CreateFilm, CreateMessage
from src.handlers import commands

dp = Dispatcher()
bot = Bot(config.token, parse_mode=ParseMode.MARKDOWN)


def set_handlers():
    dp.message.register(start_handler, CommandStart())
    # dp.message.register(commands.create_sender_handler, Command(commands=['sender']), F.from_user.id.in_(config.admin_ids))
    dp.message.register(commands.create_sender_handler, Command(commands=['sender']))
    dp.include_router(create_mail_message_router)
    dp.callback_query.register(callbacks.cancel_sending, F.data == "cancel")
    dp.callback_query.register(callbacks.all_films, F.data == "all_films")
    dp.callback_query.register(callbacks.all_films, F.data == "all_serials")
    dp.callback_query.register(callbacks.all_films_view, F.data == "view_films")
    dp.callback_query.register(callbacks.all_films_view, F.data == "view_serials")
    dp.callback_query.register(callbacks.all_films_not_view, F.data == "not_view_films")
    dp.callback_query.register(callbacks.all_films_not_view, F.data == "not_view_serials")
    dp.callback_query.register(callbacks.back_film, F.data == "back_films")
    dp.callback_query.register(callbacks.back_serial, F.data == "back_serials")
    dp.callback_query.register(callbacks.start_sending, F.data.startswith("start"), CreateMessage.confirm_sender)
    dp.callback_query.register(callbacks.create_film_or_serial, F.data.startswith("add_films"))
    dp.callback_query.register(callbacks.start_add_film, F.data.startswith("create_film"), CreateFilm.confirm_sender)
    # dp.callback_query.register(callbacks.start_add, F.data.startswith("add_films"), CreateFilm.get_text)
    dp.callback_query.register(callbacks.get_film, F.data.startswith("film:"))
    dp.callback_query.register(callbacks.update_viewed_film, F.data.startswith("viewed:"))
    dp.callback_query.register(callbacks.update_unviewed_film, F.data.startswith("unviewed:"))
    dp.callback_query.register(callbacks.delete_film, F.data.startswith("delete:"))
    dp.include_routers(commands.router)


def set_middlewares():
    dp.update.middleware(DataBaseSession(session_pool=AsyncSessionLocal))


async def main() -> None:
    set_middlewares()
    set_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())