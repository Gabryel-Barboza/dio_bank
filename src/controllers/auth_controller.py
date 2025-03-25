from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status

from src.databases.bank_db import Session, get_session
from src.services.auth_services import AuthService
from src.utils.exceptions import (
    PasswordAuthenticationFailException,
    UsernameAuthenticationFailException,
)

router = APIRouter(prefix='/auth', tags=['Auth'])

auth = AuthService()


@router.post(
    '/login',
)
async def login(
    *,
    session: Session = Depends(get_session),
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
):
    try:
        # Verificar autenticação com usuário e senha
        await auth.authenticate_user(session, username, password)
    except (
        PasswordAuthenticationFailException,
        UsernameAuthenticationFailException,
    ) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.msg)
    else:
        # Se válidos, retornar token de acesso
        return 'abcdefgh'
