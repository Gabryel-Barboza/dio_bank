import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, SQLModel

from src.settings import settings

settings.database_url = 'sqlite:///'


# Criando banco de dados
@pytest_asyncio.fixture()
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
    from src.models import Account, Transaction, TransactionType, User
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

    users_obj: list[User] = []
    for i in range(0, 3):
        user = users[i]
        user.update(hash_password(user['password']))
        users_obj.append(User(**user))

    session.add_all(users_obj)
    session.commit()

    accounts = []
    for i in range(0, 3):
        session.refresh(users_obj[i])
        accounts.append(
            Account(id_user=users_obj[i].id, account_no=len(users_obj[i].accounts))
        )

    session.add_all(accounts)
    session.commit()

    transactions_obj = []
    for i in range(0, 3):
        transactions_obj.append(
            Transaction(
                id_account=accounts[i].id,
                **transactions[0],
                transaction_no=len(accounts[i].transactions),
            )
        )

    session.add_all(transactions_obj)
    session.commit()


# Criando cliente de requisições
@pytest_asyncio.fixture()
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


# Recuperando IDs de usuários criados
# TODO: alterar fixture para ser melhor utilizada em parametrizes, onde a lista não é recriada para cada request
@pytest_asyncio.fixture
async def user_ids(client: AsyncClient, access_token: str):
    from random import randint

    response = await client.get(
        '/users/', headers={'Authorization': f'Bearer {access_token}'}
    )

    ids = [user['id'] for user in response.json()]

    return ids[randint(0, 2)]


# Fixture para recuperar IDs das contas
@pytest_asyncio.fixture
async def account_ids(client: AsyncClient, access_token: str):
    from random import randint

    response = await client.get(
        '/users/accounts/', headers={'Authorization': f'Bearer {access_token}'}
    )

    ids = [account['id'] for account in response.json()]

    return ids[randint(0, 2)]
