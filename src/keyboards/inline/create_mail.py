from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb_confirm() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отправить сейчас", callback_data=f"start"),
        InlineKeyboardButton(text="Отменить", callback_data=f"cancel"),
    )
    return builder


def get_all_films() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Все", callback_data=f"all_films"),
        InlineKeyboardButton(text="Просмотренные", callback_data=f"view_films"),
    )
    builder.row(
        InlineKeyboardButton(text="Непросмотренные", callback_data=f"not_view_films"),
        InlineKeyboardButton(text="Добавить", callback_data=f"add_films"),
    )
    return builder


def get_all_serials() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Все", callback_data=f"all_serials"),
        InlineKeyboardButton(text="Просмотренные", callback_data=f"view_serials"),
    )
    builder.row(
        InlineKeyboardButton(text="Непросмотренные", callback_data=f"not_view_serials"),
        InlineKeyboardButton(text="Добавить", callback_data=f"add_serials"),
    )
    return builder


def get_kb_add_film() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Добавить", callback_data=f"create_film"),
        InlineKeyboardButton(text="Отменить", callback_data=f"cancel_create"),
    )
    return builder


def get_kb_update_film(id_film: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отметить просмотренным ✅", callback_data=f"viewed:{id_film}")
    )
    builder.row(
        InlineKeyboardButton(text="Отметить непросмотренным ❌", callback_data=f"unviewed:{id_film}")
    )
    builder.row(
        InlineKeyboardButton(text="Удалить", callback_data=f"delete:{id_film}")
    )
    return builder