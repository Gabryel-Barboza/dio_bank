from sqlmodel import SQLModel, create_engine

# Instanciando banco
database_url = 'sqlite:///./bank.db'
debug = True
connect_args = {'check_same_thread': False}
engine = create_engine(database_url, echo=debug, connect_args=connect_args)


def create_db():
    from src.models.account_model import Account  # noqa
    from src.models.user_model import User  # noqa

    SQLModel.metadata.create_all(engine)
