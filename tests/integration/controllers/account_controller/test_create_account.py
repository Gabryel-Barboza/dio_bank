from http import HTTPStatus
from random import randint

import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize('user_id', [lf('user_ids'), lf('user_ids')])
async def test_create_account_success(
    client: AsyncClient, access_token: str, user_id: str
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
