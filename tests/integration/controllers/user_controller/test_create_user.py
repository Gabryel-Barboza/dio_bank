from http import HTTPStatus

from httpx import AsyncClient


async def test_create_user_success(client: AsyncClient):
    user = {
        'username': 'marquinhos',
        'fullname': 'Marcos Gonçalves',
        'address': 'Rua São Paulo, 09',
        'cpf': '12345678919',
        'birth_date': '2000-04-05',
        'password': '123456',
    }

    response = await client.post('/users/', json=user)
    content = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert content == {
        'address': 'Rua São Paulo, 09',
        'birth_date': '2000-04-05',
        'cpf': '12345678919',
        'fullname': 'Marcos Gonçalves',
        'id_user': 4,
        'username': 'marquinhos',
    }


async def test_create_user_obligatory_fields_fail(client: AsyncClient):
    user = {
        'address': 'Rua São Paulo, 09',
        'birth_date': '2000-04-05',
    }

    response = await client.post('/users/', json=user)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_create_user_no_password_fail(client: AsyncClient):
    user = {
        'username': 'marquinhos',
        'fullname': 'Marcos Gonçalves',
        'cpf': '12345678919',
    }

    response = await client.post('/users/', json=user)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
