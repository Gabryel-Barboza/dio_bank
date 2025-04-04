from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.databases.bank_db import Session, get_session
from src.models.user_model import AccessToken
from src.services.auth_services import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

router = APIRouter(prefix='/auth', tags=['Auth'])

auth = AuthService()


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
)
async def login(
    *,
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> AccessToken:
    username = login_data.username
    password = login_data.password

    # Verificar autenticação com usuário e senha
    access_token = await auth.authenticate_user(session, username, password)

    # Se válidos, retornar token de acesso
    return access_token


async def get_user_authentication(
    *,
    session: Session = Depends(get_session),
    token: Annotated[str, Depends(oauth2_scheme)],
):
    await auth.get_credentials_user(session, token)

    return
