from http import HTTPStatus

import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize('account_id', (lf('account_ids'), lf('account_ids')))
async def test_create_transaction_success(
    client: AsyncClient, access_token: str, account_id: str
):
    transaction = {
        'transaction': {'transaction_type': 'depósito', 'transaction_value': 100}
    }
    response = await client.post(
        f'/users/accounts/{account_id}/transactions/',
        headers={'Authorization': f'Bearer {access_token}'},
        json=transaction,
    )
    content = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert content != {}
