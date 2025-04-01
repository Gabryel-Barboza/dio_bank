from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient


async def test_delete_account_success(
    client: AsyncClient, access_token: str, account_id: int = 1
):
    response = await client.delete(
        f'/users/accounts/{account_id}/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
