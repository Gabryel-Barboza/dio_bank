from sqlmodel import Session, SQLModel, create_engine, text

from src.settings import settings

# Instanciando banco
database_url = settings.database_url
debug = settings.debug
connect_args = {}
pool = None

if 'sqlite' in settings.database_url:
    connect_args = {'check_same_thread': False}

if settings.environment == 'testing':
    from sqlmodel import StaticPool

    pool = StaticPool

engine = create_engine(
    database_url, echo=debug, connect_args=connect_args, poolclass=pool
)


def create_db():
    from src.models.account_model import Account  # noqa
    from src.models.user_model import User  # noqa
    from src.models.transaction_model import Transaction  # noqa

    SQLModel.metadata.create_all(engine)

    if 'sqlite' in settings.database_url:
        # Habilita suporte para restrições com Foreign key no SQLite
        with engine.connect() as connection:
            connection.execute(text('PRAGMA foreign_keys=ON'))


def get_session():
    with Session(engine) as session:
        yield session
