from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Instanciando banco
database_url = 'sqlite:///./bank.db'
connect_args = {'check_same_thread': False}
engine = create_engine(database_url, connect_args=connect_args)


def create_db():
    from src.models.account_model import Account  # noqa
    from src.models.user_model import User  # noqa

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# Criando objeto de sessão do banco de dados
DbSession = Annotated[Session, Depends(get_session)]
