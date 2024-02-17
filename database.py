import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str] = mapped_column(unique=False)
    added: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id", ondelete="SET NULL"))
    genre: Mapped["Genre"] = relationship(back_populates="books")
    is_read: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"Книга (title={self.title})"

    def get_status(self):
        if self.is_read == 0:
            return "Не прочитана"
        if self.is_read == 1:
            return "Прочитана"


class Genre(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    books: Mapped[List["Book"]] = relationship(back_populates="genre")

    def __repr__(self):
        return f"Жанр (name={self.name})"
