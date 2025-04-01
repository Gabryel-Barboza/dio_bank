from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import Session

from src.models import User


@pytest.mark.parametrize('user_id', [1, 2, 3])
async def test_delete_user_success(
    client: AsyncClient, session: Session, access_token: str, user_id: int
):
    response = await client.delete(
        f'/users/{user_id}', headers={'Authorization': f'Bearer {access_token}'}
    )
    user = session.get(User, user_id)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert user is None


async def test_delete_user_fail(
    client: AsyncClient, access_token: str, user_id: int = None
):
    response = await client.delete(
        f'/users/{user_id}', headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_delete_user_no_authentication(client: AsyncClient, user_id: int = 1):
    response = await client.delete(f'/users/{user_id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
