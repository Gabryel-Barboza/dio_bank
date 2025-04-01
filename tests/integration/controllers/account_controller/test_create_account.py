from http import HTTPStatus
from random import randint

import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.parametrize('user_id', (1, 2, 3))
async def test_create_account_success(
    client: AsyncClient, access_token: str, user_id: int
):
    rand = randint(1, 2)
    account = {} if rand == 1 else {'account_type': 'poupança'}

    response = await client.post(
        f'/users/{user_id}/accounts/',
        headers={'Authorization': f'Bearer {access_token}'},
        json=account,
    )
    content = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert content is not None
