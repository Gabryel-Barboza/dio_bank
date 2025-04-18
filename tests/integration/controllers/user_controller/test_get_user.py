from http import HTTPStatus

import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf


async def test_get_users_success(client: AsyncClient, access_token: str):
    response = await client.get(
        '/users/',
        params={'skip': 0, 'limit': 2},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(content) == 2


async def test_get_users_query_fail(client: AsyncClient, access_token: str):
    response = await client.get(
        '/users/',
        params={'skip': 0, 'limit': 10000},
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_users_no_authentication(client: AsyncClient):
    response = await client.get('/users/', params={'skip': 0, 'limit': 100})

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize('user_id', [lf('user_ids'), lf('user_ids')])
async def test_get_user_by_id_success(
    client: AsyncClient, access_token: str, user_id: str
):
    response = await client.get(
        f'/users/{user_id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content != {'detail': 'User not found!'}


async def test_get_user_by_id_fail(
    client: AsyncClient,
    access_token: str,
    user_id: str = '09d78ba8ec143b16b45dc817f10b94fa',
):
    response = await client.get(
        f'/users/{user_id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert content == {'detail': 'User not found!'}


async def test_get_user_by_id_no_authentication(
    client: AsyncClient, user_id: str = '09d78ba8ec143b16b45dc817f10b94fa'
):
    response = await client.get(f'/users/{user_id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_get_user_by_id_no_id_fail(
    client: AsyncClient, access_token: str, user_id: str = None
):
    response = await client.get(
        f'/users/{user_id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
