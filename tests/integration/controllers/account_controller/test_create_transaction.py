from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.parametrize('account_id', (1, 2, 3))
async def test_create_transaction_success(
    client: AsyncClient, access_token: str, account_id: int
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
