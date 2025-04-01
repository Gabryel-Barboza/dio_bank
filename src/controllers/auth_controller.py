from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.databases.bank_db import Session, get_session
from src.models.user_model import AccessToken
from src.services.auth_services import AuthService
from src.utils.exceptions import (
    CredentialsTokenException,
    PasswordAuthenticationFailException,
    UsernameAuthenticationFailException,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

router = APIRouter(prefix='/auth', tags=['Auth'])

auth = AuthService()


@router.post(
    '/login',
)
async def login(
    *,
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> AccessToken:
    try:
        username = login_data.username
        password = login_data.password

        # Verificar autenticação com usuário e senha
        access_token = await auth.authenticate_user(session, username, password)
    except (
        PasswordAuthenticationFailException,
        UsernameAuthenticationFailException,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.msg,
            headers={'WWW-Authenticate': 'Bearer'},
        )
    else:
        # Se válidos, retornar token de acesso
        return access_token


async def get_user_authentication(
    *,
    session: Session = Depends(get_session),
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        await auth.get_credentials_user(session, token)
    except CredentialsTokenException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.msg,
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return
