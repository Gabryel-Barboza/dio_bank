from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient


async def test_get_users_success(client: AsyncClient):
    response = await client.get('/users/', params={'skip': 0, 'limit': 3})
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(content) == 3


async def test_get_users_query_fail(client: AsyncClient):
    response = await client.get('/users/', params={'skip': 0, 'limit': 10000})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('user_id', [1, 2, 3])
async def test_get_user_by_id_success(client: AsyncClient, user_id: int):
    response = await client.get(f'/users/{user_id}')
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content != {'detail': 'User not found!'}


async def test_get_user_by_id_fail(client: AsyncClient, user_id: int = 90):
    response = await client.get(f'/users/{user_id}')
    content = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert content == {'detail': 'User not found!'}


async def test_get_user_by_id_no_id_fail(client: AsyncClient, user_id: int = None):
    response = await client.get(f'/users/{user_id}')

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
