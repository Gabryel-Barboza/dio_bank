from http import HTTPStatus
from uuid import UUID

import pytest
from httpx import AsyncClient
from pytest_lazy_fixtures import lf
from sqlmodel import Session

from src.models import User


@pytest.mark.parametrize('user_id', [lf('user_ids'), lf('user_ids')])
async def test_delete_user_success(
    client: AsyncClient, session: Session, access_token: str, user_id: str
):
    user_id = UUID(user_id)
    response = await client.delete(
        f'/users/{user_id}', headers={'Authorization': f'Bearer {access_token}'}
    )
    user = session.get(User, user_id)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert user is None


async def test_delete_user_fail(
    client: AsyncClient, access_token: str, user_id: str = None
):
    response = await client.delete(
        f'/users/{user_id}', headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_delete_user_no_authentication(
    client: AsyncClient, user_id: str = '09d78ba8ec143b16b45dc817f10b94fa'
):
    response = await client.delete(f'/users/{user_id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
