from sqlmodel import Session, select

from src.models.user_model import User
from src.utils.cryptography import verify_hash
from src.utils.exceptions import (
    PasswordAuthenticationFailException,
    UsernameAuthenticationFailException,
)


class AuthService:
    @staticmethod
    async def authenticate_user(session: Session, username: str, password: str) -> None:
        user = session.exec(select(User).where(User.username == username)).one()

        if not user:
            raise UsernameAuthenticationFailException

        is_password = verify_hash(password, user.password)

        if not is_password:
            raise PasswordAuthenticationFailException

        return
