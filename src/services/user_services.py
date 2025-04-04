from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.models.user_model import User
from src.utils.cryptography import hash_password
from src.utils.exceptions import BankIntegrityFailException, RegistryNotFoundException


class UserService:
    # Método para recuperar usuários
    @staticmethod
    async def read_users(
        session: Session, skip: int = 0, limit: int = 10, user_id: int = None
    ) -> list[User] | User | None:
        # Recuperar por ID
        if user_id:
            user = session.get(User, user_id)

            if not user:
                raise RegistryNotFoundException('User not found!')

            return user
        # Recuperar todos
        else:
            users = session.exec(select(User).offset(skip).limit(limit)).all()

            return users

    # Método para criar usuários
    @staticmethod
    async def insert_user(session: Session, user: dict) -> User:
        user.update(hash_password(user['password']))  # Convertendo senha para hash
        user: User = User.model_validate(user)  # Convertendo para model User
        try:
            session.add(user)
            session.commit()
        except IntegrityError as exc:
            print(exc)
            msg = str(exc).split('\n')[0].split(')')[1]
            msg, constr_error = msg.split(':')
            raise BankIntegrityFailException(msg, constr_error)
        else:
            session.refresh(user)

        return user

    # Método para atualizar usuários
    @staticmethod
    async def update_user(session: Session, user_id: int, fields: dict) -> None:
        user = session.get(User, user_id)

        if not user:
            raise RegistryNotFoundException('User not found!')

        if fields.get('password', None):
            fields.update(hash_password(fields['password']))

        user.sqlmodel_update(fields)
        try:
            session.add(user)
            session.commit()
        except IntegrityError as exc:
            print(exc)
            msg = str(exc).split('\n')[0].split(')')[1]
            msg, constr_error = msg.split(':')
            raise BankIntegrityFailException(msg, constr_error)

        return

    # Método para remover usuários.
    @staticmethod
    async def delete_user(session: Session, user_id: int) -> None:
        user = session.get(User, user_id)

        if not user:
            raise RegistryNotFoundException('User not found!')

        session.delete(user)
        session.commit()

        return
