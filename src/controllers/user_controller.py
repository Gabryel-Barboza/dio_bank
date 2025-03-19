from fastapi import APIRouter
from sqlmodel import select

from src.databases.bank_db import DbSession
from src.models.account_model import Account
from src.models.user_model import User

router = APIRouter(prefix='/users')


@router.get('/')
async def get_users(session: DbSession) -> list[User]:
    users = session.exec(select(User)).all()
    return users


@router.get('/{id}')
async def get_user_by_id(id: int, session: DbSession):
    user = session.get(User, id)
    return user


@router.post('/')
async def create_user(user: User, session: DbSession):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.patch('/')
async def update_user():
    pass


@router.delete('/')
async def delete_user(id: int, session: DbSession):
    user = session.get(User, id)
    session.delete(user)
