from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.database.engine import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    films = relationship("Film", back_populates='user')


class Film(Base):
    __tablename__ = 'film'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=False)
    id_user = Column(Integer, ForeignKey('user.id', name='fk_film_user_id'))
    id_type = Column(Integer, ForeignKey('type.id', name='fk_film_type_id'))

    user = relationship("User", back_populates='films')
    type = relationship("Type", back_populates='films')


class Type(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    films = relationship("Film", back_populates='type')
