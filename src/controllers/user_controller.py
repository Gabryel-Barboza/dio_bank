from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.databases.bank_db import Session, get_session
from src.models.user_model import (
    UserCreateModel,
    UserPatchUpdateModel,
    UserPublicAccountsModel,
    UserPublicModel,
)
from src.services.user_services import UserService
from src.utils.exceptions import RegistryNotFoundException

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
    user_id: int,
) -> UserPublicAccountsModel | None:
    try:
        user = await usr_service.read_users(session, user_id=user_id)
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found!'
        )
    else:
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
    user_id: int,
    user: UserCreateModel,
) -> None:
    try:
        await usr_service.update_user(session, user_id, user.model_dump())
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found!'
        )

    return


@router.patch(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user_fields(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    fields: UserPatchUpdateModel,
) -> None:
    try:
        await usr_service.update_user(
            session, user_id, fields.model_dump(exclude_unset=True)
        )
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found!'
        )

    return


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
) -> None:
    try:
        await usr_service.delete_user(session, user_id)
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found!'
        )
    return
