from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User, Film


async def get_active_users(session: AsyncSession):
    users = await session.execute(
        select(User.telegram_id).filter(User.is_active)
    )
    return users.scalars().all()


async def add_user(session: AsyncSession, telegram_id: str, username: str, first_name: str, last_name: str):
    is_exists = await session.execute(select(User.id).filter(User.telegram_id == telegram_id))
    is_exists = is_exists.scalar()
    if is_exists:
        return False

    user = User(
        telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name
    )
    session.add(user)
    await session.commit()
    return user


async def change_active(session: AsyncSession, user_id: str, is_active: bool) -> None:
    await session.execute(update(User).filter(User.telegram_id == user_id).values(is_active=is_active))
    await session.commit()


async def get_films(session: AsyncSession, telegram_id: str, id_type: int):
    id_user = await session.execute(select(User.id).filter(User.telegram_id == telegram_id))
    id_user = id_user.scalar()
    print(f'{telegram_id} это ид пользователя')

    all_films = await session.execute(select(Film.id, Film.name, Film.status).filter(Film.id_user==id_user, Film.id_type==id_type))
    all_films = all_films.all()
    print(f'{all_films} фильмы')
    return all_films


async def get_films_view(session: AsyncSession, telegram_id: str, id_type: int):
    id_user = await session.execute(select(User.id).filter(User.telegram_id == telegram_id))
    id_user = id_user.scalar()
    print(f'{telegram_id} это ид пользователя')

    all_films = await session.execute(select(Film.id, Film.name, Film.status).filter(Film.id_user==id_user, Film.status == True, Film.id_type==id_type))
    all_films = all_films.all()
    print(f'{all_films} фильмы')
    return all_films
    
async def get_films_not_view(session: AsyncSession, telegram_id: str, id_type: int):
    id_user = await session.execute(select(User.id).filter(User.telegram_id == telegram_id))
    id_user = id_user.scalar()
    print(f'{telegram_id} это ид пользователя')

    all_films = await session.execute(select(Film.id, Film.name, Film.status).filter(Film.id_user==id_user, Film.status == False, Film.id_type==id_type))
    all_films = all_films.all()
    print(f'{all_films} фильмы')
    return all_films


async def add_film_or_serial(session: AsyncSession, telegram_id: str, name: str, id_type: int):
    id_user = await session.execute(select(User.id).filter(User.telegram_id == telegram_id))
    id_user = id_user.scalar()

    film = Film(
        name=name, id_user=id_user, id_type=id_type
    )
    session.add(film)
    await session.commit()
    return film


async def get_film_by_id(session: AsyncSession, id_film: int):
    film = await session.execute(select(Film.id, Film.name, Film.status).filter(Film.id==id_film))
    film = film.first()
    print(f'{film} фильмы')
    return film


async def update_view_film_by_id(session: AsyncSession, id_film: int):
    film = await session.execute(select(Film).filter(Film.id==id_film))
    film = film.scalar()
    film.status = True
    session.add(film)
    await session.commit()
    return film


async def update_unview_film_by_id(session: AsyncSession, id_film: int):
    film = await session.execute(select(Film).filter(Film.id==id_film))
    film = film.scalar()
    film.status = False
    session.add(film)
    await session.commit()
    return film


async def delete_film_by_id(session: AsyncSession, id_film: int):
    film = await session.execute(select(Film).filter(Film.id==id_film))
    film = film.scalar()
    if film:
        await session.delete(film)
        await session.commit()
        return 'ok'
    else:
        return 'Film not found'