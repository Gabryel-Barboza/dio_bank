from http import HTTPStatus
from uuid import UUID

import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf
from sqlmodel import Session

from src.models import Account


@pytest.mark.parametrize('account_id', [lf('account_ids'), lf('account_ids')])
async def test_delete_account_success(
    session: Session, client: AsyncClient, access_token: str, account_id: str
):
    account_id = UUID(account_id)
    response = await client.delete(
        f'/users/accounts/{account_id}/',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    account = session.get(Account, account_id)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert account is None
