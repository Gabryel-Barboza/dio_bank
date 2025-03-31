from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import Session

from src.models import User


@pytest.mark.parametrize('user_id', [1, 2, 3])
async def test_delete_user_success(client: AsyncClient, session: Session, user_id: int):
    response = await client.delete(f'/users/{user_id}')
    user = session.get(User, user_id)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert user is None


async def test_delete_user_fail(client: AsyncClient, user_id: int = None):
    response = await client.delete(f'/users/{user_id}')

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
