import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, SQLModel

from src.settings import settings

settings.database_url = 'sqlite:///'
settings.environment = 'testing'
settings.debug = False


# Criando banco de dados
@pytest_asyncio.fixture
async def db(request):
    # Permite carregar as configurações de settings antes de criar a engine na importação
    from src.databases.bank_db import create_db, engine

    create_db()
    yield
    SQLModel.metadata.drop_all(engine)


# Recebendo sessões
@pytest_asyncio.fixture
async def session():
    from src.databases.bank_db import get_session

    for session in get_session():
        return session


# Populando banco de dados antes dos testes
@pytest_asyncio.fixture()
async def populate_db(
    session: Session,
):
    from random import randint

    from src.controllers import account_controller, user_controller
    from src.models import AccountCreateModel, TransactionCreateModel, UserCreateModel

    users = [
        {
            'fullname': 'Gabryel B',
            'username': 'gabryel',
            'cpf': '12345678910',
            'password': '123456',
        },
        {
            'fullname': 'Kaio Silva',
            'username': 'kaio',
            'cpf': '12345678911',
            'password': '123456',
        },
        {
            'fullname': 'Brayan Gomes',
            'username': 'brayan',
            'cpf': '12345678912',
            'password': '654321',
        },
    ]
    accounts = [{'account_type': 'poupança'}, {}]
    transactions = [
        {'transaction_type': 'depósito', 'transaction_value': 1000.00},
        {'transaction_type': 'depósito', 'transaction_value': 200.00},
        {'transaction_type': 'depósito', 'transaction_value': 50.00},
        {'transaction_type': 'saque', 'transaction_value': 100.00},
        {'transaction_type': 'saque', 'transaction_value': 50.00},
        {'transaction_type': 'saque', 'transaction_value': 300.00},
    ]

    for i in range(0, 3):
        user = UserCreateModel.model_validate(users[i])
        await user_controller.create_user(session=session, user=user)

        for j in range(0, randint(1, 2)):
            account = AccountCreateModel.model_validate(accounts[j])
            await account_controller.create_account(
                session=session,
                account=account,
                user_id=i + 1,
            )

        transaction = TransactionCreateModel.model_validate(transactions[0])
        await account_controller.create_transaction(
            session=session, id_account=i + 1, transaction=transaction
        )


# Criando cliente de requisições
@pytest_asyncio.fixture
async def client(db, populate_db):
    from src.main import app

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    async with AsyncClient(
        base_url='http://test',
        transport=ASGITransport(app=app),
        headers=headers,
    ) as client:
        yield client
