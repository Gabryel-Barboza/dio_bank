from http import HTTPStatus

import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize('user_id', [lf('user_ids'), lf('user_ids'), lf('user_ids')])
async def test_update_user_success(
    client: AsyncClient, access_token: str, user_id: str
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
    client: AsyncClient,
    access_token: str,
    user_id: str = '09d78ba8ec143b16b45dc817f10b94fa',
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


async def test_update_user_no_authentication(
    client: AsyncClient, user_id: str = '09d78ba8ec143b16b45dc817f10b94fa'
):
    fields = {
        'username': 'marquinhos',
        'fullname': 'Marcos Gonçalves',
        'cpf': '12345678919',
        'password': '456',
    }

    response = await client.put(f'/users/{user_id}', json=fields)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize('user_id', [lf('user_ids'), lf('user_ids')])
async def test_update_user_fields_success(
    client: AsyncClient, access_token: str, user_id: str
):
    fields = {'username': 'marquinhos', 'address': 'rua tal'}

    response = await client.patch(
        f'/users/{user_id}',
        json=fields,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


async def test_update_user_fields_fail(
    client: AsyncClient, access_token: str, user_id: str = None
):
    fields = {'username': 'marquinhos'}

    response = await client.patch(
        f'/users/{user_id}',
        json=fields,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_update_user_fields_no_authentication(
    client: AsyncClient, user_id: str = '09d78ba8ec143b16b45dc817f10b94fa'
):
    fields = {'username': 'marquinhos', 'address': 'rua tal'}

    response = await client.patch(f'/users/{user_id}', json=fields)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
