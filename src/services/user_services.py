from sqlmodel import Session, select, update

from src.databases.bank_db import engine
from src.models.user_model import User
from src.utils.exceptions import RegistryNotFoundException


# TODO: escolher algoritmo de hash
def hash_password(user: dict) -> dict:
    password = user['password']
    hashed_password = {'password': password}

    return hashed_password


class UserService:
    # Método para recuperar usuários
    @staticmethod
    async def read_users(
        skip: int = 0, limit: int = 10, user_id: int = None
    ) -> list[User] | User | None:
        with Session(engine) as session:
            # Recuperar por ID
            if user_id:
                user = session.get(User, user_id)

                if not user:
                    raise RegistryNotFoundException

                return user
            # Recuperar todos
            else:
                users = session.exec(select(User).offset(skip).limit(limit)).all()

                return users

    # Método para criar usuários
    @staticmethod
    async def insert_user(user: dict) -> None:
        with Session(engine) as session:
            user.update(hash_password(user))
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
                if fields['password']:
                    fields.update(hash_password(fields))

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
