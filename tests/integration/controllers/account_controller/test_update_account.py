from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient


async def test_update_account_success(
    client: AsyncClient, access_token: str, account_id: int = 1
):
    fields = {'account_type': 'poupança', 'balance': 10.00}
    response = await client.put(
        f'/users/accounts/{account_id}/',
        headers={'Authorization': f'Bearer {access_token}'},
        json=fields,
    )

    assert response.status_code == HTTPStatus.CREATED
