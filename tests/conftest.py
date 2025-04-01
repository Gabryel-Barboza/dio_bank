import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, SQLModel

from src.settings import settings

settings.database_url = 'sqlite:///'


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
    from src.models import Account, AccountType, Transaction, TransactionType, User
    from src.utils.cryptography import hash_password

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
    transactions = [
        {'transaction_type': TransactionType.deposito, 'transaction_value': 1000.00},
        {'transaction_type': TransactionType.deposito, 'transaction_value': 200.00},
        {'transaction_type': TransactionType.deposito, 'transaction_value': 50.00},
        {'transaction_type': TransactionType.saque, 'transaction_value': 100.00},
        {'transaction_type': TransactionType.saque, 'transaction_value': 50.00},
        {'transaction_type': TransactionType.saque, 'transaction_value': 300.00},
    ]

    for i in range(0, 3):
        user = users[i]
        password = hash_password(user['password'])

        user.update(password)
        user = User(**user)
        session.add(user)

    session.add_all(
        [
            Account(id_user=1),
            Account(id_user=1, account_type=AccountType.poupanca),
            Account(id_user=2),
            Account(id_user=2),
            Account(id_user=3),
        ]
    )

    session.add_all(
        [
            Transaction(id_account=1, **transactions[0]),
            Transaction(id_account=1, **transactions[3]),
            Transaction(id_account=2, **transactions[0]),
            Transaction(id_account=2, **transactions[3]),
            Transaction(id_account=3, **transactions[1]),
            Transaction(id_account=4, **transactions[0]),
            Transaction(id_account=5, **transactions[1]),
            Transaction(id_account=5, **transactions[5]),
        ]
    )
    session.commit()


# Criando cliente de requisições
@pytest_asyncio.fixture
async def client(db, populate_db):
    from src.main import app

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    async with AsyncClient(
        base_url='http://test',
        transport=ASGITransport(app=app),
        headers=headers,
    ) as client:
        yield client


# Criando access_token para autenticação de rotas
@pytest_asyncio.fixture
async def access_token(client: AsyncClient):
    data = {'username': 'gabryel', 'password': '123456'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = await client.post('/auth/login', data=data, headers=headers)
    access_token = response.json()['access_token']

    return access_token
