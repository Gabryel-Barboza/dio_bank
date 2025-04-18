from http import HTTPStatus

import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize(
    'account_id',
    [lf('account_ids'), lf('account_ids')],
)
async def test_get_account_transactions_success(
    client: AsyncClient, access_token: str, account_id: str
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content != []


async def test_get_account_transactions_no_id_fail(
    client: AsyncClient, access_token: str, account_id: str = None
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_account_transactions_no_authentication(
    client: AsyncClient, account_id: str = 0
):
    response = await client.get(f'/users/accounts/{account_id}/transactions/')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    'account_id,transaction_no',
    [(lf('account_ids'), 1), (lf('account_ids'), 1), (lf('account_ids'), 1)],
)
async def test_get_account_transaction_success(
    client: AsyncClient, access_token: str, account_id: str, transaction_no: int
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/{transaction_no}',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    content = response.json()

    assert response.status_code == HTTPStatus.OK
    assert content is not None


async def test_get_account_transaction_no_transaction_number_fail(
    client: AsyncClient,
    access_token: str,
    account_id: str = lf('account_ids'),
    transaction_no: int = None,
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/{transaction_no}',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_account_transaction_no_authentication(
    client: AsyncClient,
    account_id: str = '152f14e5eae33b97fafd0158f7c74a84',
    transaction_no: int = 1,
):
    response = await client.get(
        f'/users/accounts/{account_id}/transactions/{transaction_no}'
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
