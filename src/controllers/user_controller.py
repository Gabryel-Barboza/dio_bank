from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.controllers.auth_controller import get_user_authentication
from src.databases.bank_db import Session, get_session
from src.models.user_model import (
    UserCreateModel,
    UserPatchUpdateModel,
    UserPublicAccountsModel,
    UserPublicModel,
)
from src.services.user_services import UserService

router = APIRouter(prefix='/users', tags=['User'])
usr_service = UserService()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
)
async def get_users(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = Query(
        default=100, le=100
    ),  # Recebe 100 por padrão, valida valores de no máximo 100
    token: Annotated[str, Depends(get_user_authentication)],
) -> list[UserPublicAccountsModel] | None:
    users = await usr_service.read_users(session, skip, limit)

    return users


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    *,
    session: Session = Depends(get_session),
    user_id: UUID,
    token: Annotated[str, Depends(get_user_authentication)],
) -> UserPublicAccountsModel | None:
    user = await usr_service.read_users(session, user_id=user_id)

    return user


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    *,
    session: Session = Depends(get_session),
    user: UserCreateModel,
) -> UserPublicModel:
    user = await usr_service.insert_user(session, user.model_dump())

    return user


@router.put(
    '/{user_id}',
    status_code=status.HTTP_201_CREATED,
)
async def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: UUID,
    token: Annotated[str, Depends(get_user_authentication)],
    user: UserCreateModel,
) -> None:
    await usr_service.update_user(session, user_id, user.model_dump())

    return


@router.patch(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user_fields(
    *,
    session: Session = Depends(get_session),
    user_id: UUID,
    token: Annotated[str, Depends(get_user_authentication)],
    fields: UserPatchUpdateModel,
) -> None:
    await usr_service.update_user(
        session, user_id, fields.model_dump(exclude_unset=True)
    )

    return


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    *,
    session: Session = Depends(get_session),
    user_id: UUID,
    token: Annotated[str, Depends(get_user_authentication)],
) -> None:
    await usr_service.delete_user(session, user_id)

    return
