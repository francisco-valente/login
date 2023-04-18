''' 
    Definição das bases de dados
    Autor: Francisco
    Data: 24 fev 2023
'''

from typing import List
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime

# Parâmetros para criar/acessar o banco de dados sistemalogin
USER="root"
PASSWORD=""
HOST="localhost"
PORT=3306
BD="login_system"

CONN = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{BD}'

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


# Cadastro de Usuários
class User(Base):
    __tablename__ = "user"
    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(100))

    login: Mapped[List["Login"]] = relationship(back_populates="user", cascade="all, delete-orphan")

# Cadastro de Login
class Login(Base):
    __tablename__ = "login"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(100))
    lastLogin: Mapped[datetime] 
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="login")


Base.metadata.create_all(engine)
