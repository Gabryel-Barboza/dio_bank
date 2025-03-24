from fastapi import APIRouter, HTTPException, status

from src.models.user_model import User
from src.schemas.user_schemas import UserUpdateModel
from src.services.user_services import UserService
from src.utils.exceptions import RegistryNotFoundException

router = APIRouter(prefix='/users', tags=['User'])
usr_service = UserService()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
)
async def get_users() -> list[User] | None:
    users = await usr_service.read_users()

    return users


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(user_id: int) -> User | None:
    user = await usr_service.read_users(user_id=user_id)

    return user


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: User) -> User:
    await usr_service.insert_user(user)

    return user


@router.put(
    '/{user_id}',
    status_code=status.HTTP_201_CREATED,
)
async def update_user(user_id: int, user: User) -> None:
    try:
        await usr_service.update_user(user_id, user.model_dump())
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found!'
        )

    return


@router.patch(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
)
async def update_user_fields(user_id: int, fields: UserUpdateModel) -> None:
    try:
        await usr_service.update_user(user_id, fields.model_dump(exclude_unset=True))
    except RegistryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found!'
        )

    return


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: int) -> None:
    await usr_service.delete_user(user_id)

    return
