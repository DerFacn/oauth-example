from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    sub: Mapped[int] = mapped_column(default=0)
    username: Mapped[str] = mapped_column(String(40))
    password: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(String(256), nullable=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    picture: Mapped[str] = mapped_column(nullable=True)
