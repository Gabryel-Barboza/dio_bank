from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient


async def test_get_accounts_success(client: AsyncClient, access_token: str):
    response = await client.get(
        '/users/accounts/', headers={'Authorization': f'Bearer {access_token}'}
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(content) == 5


async def test_get_accounts_no_authentication(client: AsyncClient):
    response = await client.get('/users/accounts/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize('user_id', [1, 2, 3])
async def test_get_user_accounts_success(
    client: AsyncClient, access_token: str, user_id: int
):
    response = await client.get(
        f'/users/{user_id}/accounts/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content != []


async def test_get_user_accounts_fail(
    client: AsyncClient, access_token: str, user_id: int = None
):
    response = await client.get(
        f'/users/{user_id}/accounts/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_user_accounts_no_authentication(
    client: AsyncClient, user_id: int = 1
):
    response = await client.get(f'/users/{user_id}/accounts/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize('id_account', (1, 2, 3, 4, 5))
async def test_get_account_success(
    client: AsyncClient, access_token: str, id_account: int
):
    response = await client.get(
        f'/users/accounts/{id_account}/',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content is not None


async def test_get_account_fail(
    client: AsyncClient, access_token: str, id_account: int = None
):
    response = await client.get(
        f'/users/accounts/{id_account}/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_account_no_authentication(client: AsyncClient, id_account: int = 1):
    response = await client.get(f'/users/accounts/{id_account}/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
