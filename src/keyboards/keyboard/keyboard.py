from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


def get_start() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Фильмы"),
        KeyboardButton(text="Сериалы")
    )
    return builder