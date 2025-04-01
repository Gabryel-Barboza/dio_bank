from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.parametrize('account_id', (1, 2, 3))
async def test_get_account_transactions_success(
    client: AsyncClient, access_token: str, account_id: int
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content != []


async def test_get_account_transactions_no_id_fail(
    client: AsyncClient, access_token: str, account_id: int = None
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_account_transactions_no_authentication(
    client: AsyncClient, account_id: int = int
):
    response = await client.get(f'/users/accounts/{account_id}/transactions/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    'account_id,transaction_id', [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1)]
)
async def test_get_account_transaction_success(
    client: AsyncClient, access_token: str, account_id: int, transaction_id: int
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/{transaction_id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content is not None


async def test_get_account_transaction_no_transaction_id_fail(
    client: AsyncClient,
    access_token: str,
    account_id: int = 1,
    transaction_id: int = None,
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/{transaction_id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_account_transaction_no_authentication(
    client: AsyncClient,
    account_id: int = 1,
    transaction_id: int = 1,
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/{transaction_id}'
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
