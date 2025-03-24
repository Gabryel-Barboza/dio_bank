from sqlmodel import Session, select, update

from src.databases.bank_db import engine
from src.models.user_model import User
from src.utils.exceptions import RegistryNotFoundException


class UserService:
    # Método para recuperar usuários
    @staticmethod
    async def read_users(user_id: int = None) -> list[User] | User | None:
        with Session(engine) as session:
            # Recuperar por ID
            if user_id:
                user = session.get(User, user_id)

                return user
            # Recuperar todos
            else:
                users = session.exec(select(User)).all()

                return users

    # Método para criar usuários
    @staticmethod
    async def insert_user(user: dict) -> None:
        with Session(engine) as session:
            session.add(user)
            session.commit()

            session.refresh(user)

            return

    # Método para atualizar usuários
    @staticmethod
    async def update_user(user_id: int, fields: dict) -> None:
        with Session(engine) as session:
            user = session.get(User, user_id)

            if user:
                session.exec(
                    update(User).where(User.c.user_id == user_id).values(**fields)
                )
                session.commit()

                return
            else:
                raise RegistryNotFoundException

    # Método para remover usuários.
    @staticmethod
    async def delete_user(user_id: int) -> None:
        with Session(engine) as session:
            user = session.get(user_id)

            if user:
                session.delete(user)
                session.commit()

            return
