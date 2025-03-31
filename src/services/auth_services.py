from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select

from src.models.user_model import AccessToken, User
from src.settings import settings
from src.utils.cryptography import verify_hash
from src.utils.exceptions import (
    CredentialsTokenException,
    PasswordAuthenticationFailException,
    UsernameAuthenticationFailException,
)

# Gere uma secret key com openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class AuthService:
    # método para autenticar usuários
    async def authenticate_user(
        self, session: Session, username: str, password: str
    ) -> None:
        user = session.exec(select(User).where(User.username == username)).one_or_none()

        if not user:
            raise UsernameAuthenticationFailException

        is_password = verify_hash(password, user.password)

        if not is_password:
            raise PasswordAuthenticationFailException

        access_expire_minutes = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await self.create_access_token(
            {'sub': username}, expires_delta=access_expire_minutes
        )

        return AccessToken(access_token=access_token, token_type='bearer')

    # método para criar tokens
    @staticmethod
    async def create_access_token(
        data: dict, expires_delta: timedelta | None = None
    ) -> AccessToken:
        # Definindo tempo padrão de expiração, a partir da data atual
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=30)

        data.update({'exp': expire})
        encoded = jwt.encode(data, SECRET_KEY, ALGORITHM)

        return encoded

    # método para validar tokens de acesso
    @staticmethod
    async def get_credentials_user(session: Session, token: str) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
            username = payload.get('sub')

        except InvalidTokenError:
            raise CredentialsTokenException
        else:
            if username is None:
                raise CredentialsTokenException

            user = session.exec(select(User).where(User.username == username))

            if not user:
                raise CredentialsTokenException

            return user
