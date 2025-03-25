from sqlmodel import Session, SQLModel, create_engine, text

# Instanciando banco
# TODO: carregar configurações via .env
database_url = 'sqlite:///./bank.db'
debug = True
connect_args = {'check_same_thread': False}
engine = create_engine(database_url, echo=debug, connect_args=connect_args)


def create_db():
    from src.models.account_model import Account  # noqa
    from src.models.user_model import User  # noqa
    from src.models.transaction_model import Transaction  # noqa

    SQLModel.metadata.create_all(engine)
    # Habilita suporte para restrições com Foreign key no SQLite
    with engine.connect() as connection:
        connection.execute(text('PRAGMA foreign_keys=ON'))


def get_session():
    with Session(engine) as session:
        yield session
