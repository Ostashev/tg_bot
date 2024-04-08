from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.keyboards.inline.create_mail import get_all_films, get_all_serials
from src.states.base import CreateMessage
from aiogram import Router, F
from aiogram.filters import Command


router = Router()


async def create_sender_handler(message: Message, state: FSMContext) -> None:
    await message.answer('*Создание рассылки!*\n\nНиже отправьте текст рассылки', parse_mode=ParseMode.MARKDOWN)
    await state.set_state(CreateMessage.get_text)


async def create_film_or_serial(message: Message, state: FSMContext) -> None:
    await message.answer('*Напишите название ниже*', parse_mode=ParseMode.MARKDOWN)
    await state.set_state(CreateMessage.get_text)



@router.message(F.text.lower() == "фильмы")
async def films(message: Message):
    await message.answer(
        "Выберите какие вас интересуют фильмы",
        reply_markup=get_all_films().as_markup()
    )


@router.message(F.text.lower() == "сериалы")
async def serials(message: Message):
    await message.answer(
        "Выберите какие вас интересуют сериалы",
        reply_markup=get_all_serials().as_markup()
    )
    