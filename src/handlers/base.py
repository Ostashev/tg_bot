from aiogram.types import Message
from aiogram.utils.markdown import bold
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.requests import add_user
from src.keyboards.keyboard.keyboard import get_start


async def start_handler(message: Message, session: AsyncSession) -> None:
    await message.answer(f"Привет!, {bold(message.from_user.full_name)}!")
    await add_user(
        session,
        str(message.from_user.id),
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )

    await message.answer(
        "Здесь вы можете сохранить фильмы и сериалы.",
        reply_markup=get_start().as_markup(resize_keyboard=True)
    )