from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('user_id', [1, 2, 3])
async def test_update_user_success(
    client: AsyncClient, access_token: str, user_id: int
):
    fields = {
        'username': 'marquinhos',
        'fullname': 'Marcos Gonçalves',
        'cpf': '12345678919',
        'password': '456',
    }

    response = await client.put(
        f'/users/{user_id}',
        json=fields,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() is None


async def test_update_user_fail(
    client: AsyncClient, access_token: str, user_id: int = 1
):
    fields = {
        'username': 'marquinhos',
    }

    response = await client.put(
        f'/users/{user_id}',
        json=fields,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_update_user_no_authentication(client: AsyncClient, user_id: int = 1):
    fields = {
        'username': 'marquinhos',
        'fullname': 'Marcos Gonçalves',
        'cpf': '12345678919',
        'password': '456',
    }

    response = await client.put(f'/users/{user_id}', json=fields)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize('user_id', [1, 2, 3])
async def test_update_user_fields_success(
    client: AsyncClient, access_token: str, user_id: int
):
    fields = {'username': 'marquinhos', 'address': 'rua tal'}

    response = await client.patch(
        f'/users/{user_id}',
        json=fields,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


async def test_update_user_fields_fail(
    client: AsyncClient, access_token: str, user_id: int = None
):
    fields = {'username': 'marquinhos'}

    response = await client.patch(
        f'/users/{user_id}',
        json=fields,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_update_user_fields_no_authentication(
    client: AsyncClient, user_id: int = 1
):
    fields = {'username': 'marquinhos', 'address': 'rua tal'}

    response = await client.patch(f'/users/{user_id}', json=fields)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
