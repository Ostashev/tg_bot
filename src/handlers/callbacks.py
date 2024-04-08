import time
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.requests import add_film_or_serial, delete_film_by_id, get_active_users, get_film_by_id, get_films, get_films_not_view, get_films_view, update_unview_film_by_id, update_view_film_by_id
from src.keyboards.inline.create_mail import get_all_films, get_all_serials, get_kb_confirm, get_kb_update_film
from src.states.base import CreateFilm, CreateMessage
from src.utils import sender
from src.main import bot
# from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def cancel_sending(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Рассылка отменена(')
    await state.clear()
    await callback.answer()


async def start_sending(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await callback.message.answer('Рассылка началась')
    await state.clear()
    await callback.answer()

    user_ids = await get_active_users(session)
    t_start = time.time()
    message_id = data.get('message_id')
    count = await sender.start_sender(
        session=session,
        bot=bot,
        data=data,
        user_ids=user_ids,
        from_chat_id=callback.message.chat.id,
        message_id=message_id)
    await callback.message.answer(f'Отправлено {count}/{len(user_ids)} за {round(time.time() - t_start)}с')


async def all_films(callback: CallbackQuery, state: FSMContext, session=AsyncSession):
    # await callback.message.edit_text('Рассылка отменена(')
    # await callback.answer(reply_markup=get_all_films().as_markup())
    # print(f'{callback.data} данные!!!')
    if callback.data == 'all_films':
        id_type = 1
    elif callback.data == 'all_serials':
        id_type = 2
    
    films = await get_films(session=session, telegram_id=str(callback.from_user.id), id_type=id_type)
    if films:
        buttons = []  # Создаем список для хранения кнопок
        for film_id, film_name, film_status in films:
            button = InlineKeyboardButton(text=f'{film_name} - ✅' if film_status == True else f'{film_name} - ❌', callback_data=f"film:{film_id}")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        
        if callback.data == 'all_films':
            button = InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_films")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        elif callback.data == 'all_serials':
            button = InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_serials")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        
        # Создаем объект клавиатуры и передаем список кнопок в него
        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await callback.message.answer('Все фильмы:' if callback.data == 'all_films' else 'Все сериалы:', reply_markup=reply_markup, show_alert=True, parse_mode=ParseMode.MARKDOWN)
        await callback.answer()
    else:
        await callback.message.answer('Нет доступных фильмов.')


async def all_films_view(callback: CallbackQuery, state: FSMContext, session=AsyncSession):
    # await callback.message.edit_text('Рассылка отменена(')
    # await callback.answer(reply_markup=get_all_films().as_markup())
    if callback.data == 'view_films':
        id_type = 1
    elif callback.data == 'view_serials':
        id_type = 2
    films = await get_films_view(session=session, telegram_id=str(callback.from_user.id), id_type=id_type)
    if films:
        buttons = []  # Создаем список для хранения кнопок
        for film_id, film_name, film_status in films:
            button = InlineKeyboardButton(text=f'{film_name} - ✅' if film_status == True else f'{film_name} - ❌', callback_data=f"film:{film_id}")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        if callback.data == 'view_films':
            button = InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_films")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        elif callback.data == 'view_serials':
            button = InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_serials")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        
        # Создаем объект клавиатуры и передаем список кнопок в него
        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await callback.message.answer('Просмотренные фильмы:' if callback.data == 'view_films' else 'Просмотренные сериалы:', reply_markup=reply_markup, show_alert=True)
        await callback.answer()
    else:
        buttons = []
        button = InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_films") if callback.data == 'view_films' else InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_serials")
        buttons.append([button])
        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.answer('Нет доступных фильмов.' if callback.data == 'view_films' else 'Нет доступных сериалов.', reply_markup=reply_markup, show_alert=True)


async def all_films_not_view(callback: CallbackQuery, state: FSMContext, session=AsyncSession):
    # await callback.message.edit_text('Рассылка отменена(')
    # await callback.answer(reply_markup=get_all_films().as_markup())
    if callback.data == 'not_view_films':
        id_type = 1
    elif callback.data == 'not_view_serials':
        id_type = 2
    films = await get_films_not_view(session=session, telegram_id=str(callback.from_user.id), id_type=id_type)
    if films:
        buttons = []  # Создаем список для хранения кнопок
        for film_id, film_name, film_status in films:
            button = InlineKeyboardButton(text=f'{film_name} - ✅' if film_status == True else f'{film_name} - ❌', callback_data=f"film:{film_id}")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        if callback.data == 'not_view_films':
            button = InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_films")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        elif callback.data == 'not_view_serials':
            button = InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_serials")
            buttons.append([button])  # Добавляем каждую кнопку в отдельный список
        
        # Создаем объект клавиатуры и передаем список кнопок в него
        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await callback.message.answer('Непросмотренные фильмы:' if callback.data == 'not_view_films' else 'Непросмотренные сериалы:', reply_markup=reply_markup, show_alert=True)
        await callback.answer()
    else:
        await callback.message.answer('Нет доступных фильмов.')


async def back_film(callback: CallbackQuery, state: FSMContext):
    # await callback.message.edit_text('Рассылка отменена(')
    # print(f'{callback.data} данные!!!')
    await callback.message.answer("Выберите какие вас интересуют фильмы",
        reply_markup=get_all_films().as_markup(), show_alert=True)
    await callback.answer()


async def back_serial(callback: CallbackQuery, state: FSMContext):
    # await callback.message.edit_text('Рассылка отменена(')
    # print(f'{callback.data} данные!!!')
    await callback.message.answer("Выберите какие вас интересуют сериалы",
        reply_markup=get_all_serials().as_markup(), show_alert=True)
    await callback.answer()


# async def add_films_or_serials(callback: CallbackQuery, state: FSMContext, session=AsyncSession):
#     # await callback.message.edit_text('Рассылка отменена(')
#     # await callback.answer(reply_markup=get_all_films().as_markup())
#     if callback.data == 'add_films':
#         id_type = 1
#     elif callback.data == 'all_serials':
#         id_type = 2
#     # new_f_or_s = await add_film_or_serial(session=session, telegram_id=str(callback.from_user.id), name)
#     await message.answer('*Создание рассылки!*\n\nНиже отправьте текст рассылки', parse_mode=ParseMode.MARKDOWN)
#     await state.set_state(CreateMessage.get_text)



async def create_film_or_serial(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('*Напишите название ниже*', parse_mode=ParseMode.MARKDOWN)
    await state.set_state(CreateFilm.get_text)


async def start_add_film(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    # await callback.message.answer('Добавление началось')
    await state.clear()
    await callback.answer()

    print(data)
    
    name = data.get('msg_text')
    print(name)
    if callback.data == 'create_film':
        id_type = 1
    else:
        id_type = 2
    await add_film_or_serial(session=session, telegram_id=str(callback.from_user.id), name=name, id_type=id_type)

    await callback.message.answer(f'Добавлено!')


async def get_film(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    id_film = int(callback.data.split(":")[1])
    film = await get_film_by_id(session=session, id_film=id_film)
    await callback.message.answer(
        f'{film.name}',
        reply_markup=get_kb_update_film(id_film=id_film).as_markup(),
        show_alert=True)

    
async def update_viewed_film(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    id_film = int(callback.data.split(":")[1])
    film = await update_view_film_by_id(session=session, id_film=id_film)

    await callback.message.answer(
        f'{film.name} - ✅' if film.status == True else f'{film.name} - ❌'
        )
    

async def update_unviewed_film(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    id_film = int(callback.data.split(":")[1])
    film = await update_unview_film_by_id(session=session, id_film=id_film)

    await callback.message.answer(
        f'{film.name} - ✅' if film.status == True else f'{film.name} - ❌'
        )


async def delete_film(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    id_film = int(callback.data.split(":")[1])
    await delete_film_by_id(session=session, id_film=id_film)

    await callback.message.answer(
        f'Фильм удален!'
        )
