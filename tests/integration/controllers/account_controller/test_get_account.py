from http import HTTPStatus

import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf


async def test_get_accounts_success(client: AsyncClient, access_token: str):
    response = await client.get(
        '/users/accounts/', headers={'Authorization': f'Bearer {access_token}'}
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(content) == 3


async def test_get_accounts_no_authentication(client: AsyncClient):
    response = await client.get('/users/accounts/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize('user_id', [lf('user_ids'), lf('user_ids')])
async def test_get_user_accounts_success(
    client: AsyncClient, access_token: str, user_id: str
):
    response = await client.get(
        f'/users/{user_id}/accounts/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content != []


async def test_get_user_accounts_fail(
    client: AsyncClient, access_token: str, user_id: str = None
):
    response = await client.get(
        f'/users/{user_id}/accounts/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_user_accounts_no_authentication(
    client: AsyncClient, user_id: str = '152f14e5eae33b97fafd0158f7c74a84'
):
    response = await client.get(f'/users/{user_id}/accounts/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    'account_id', [lf('account_ids'), lf('account_ids'), lf('account_ids')]
)
async def test_get_account_success(
    client: AsyncClient, access_token: str, account_id: str
):
    response = await client.get(
        f'/users/accounts/{account_id}/',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content is not None


async def test_get_account_fail(
    client: AsyncClient, access_token: str, account_id: str = None
):
    response = await client.get(
        f'/users/accounts/{account_id}/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_account_no_authentication(
    client: AsyncClient, account_id: str = '152f14e5eae33b97fafd0158f7c74a84'
):
    response = await client.get(f'/users/accounts/{account_id}/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
