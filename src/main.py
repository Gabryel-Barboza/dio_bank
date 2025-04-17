from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .controllers import account_controller, auth_controller, user_controller
from .databases.bank_db import create_db
from .utils.exceptions import (
    BankIntegrityFailException,
    CredentialsTokenException,
    ExceedUserAccountsException,
    InsufficientBalanceException,
    InvalidOperationException,
    NonPositiveTransactionValueException,
    PasswordAuthenticationFailException,
    RegistryNotFoundException,
    UsernameAuthenticationFailException,
    UserNotFoundException,
)


# Database and other configs
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


# App Instance
app = FastAPI(
    title='DIO Bank API',
    summary='API to make transactional requests, also manipulate users and accounts.',
    version='0.1.0',
    description="""

""",
    openapi_tags='',
    openapi_url='/doc',  # /docs - Swagger, /redoc
    lifespan=lifespan,
)

# Routing

app.include_router(user_controller.router)
app.include_router(account_controller.router)
app.include_router(auth_controller.router)

# App run with fastapi dev src/main.py or
# uvicorn src.main:app --reload [--lifespan on # debug de lifespan]

# Handling exceptions


@app.exception_handler(RegistryNotFoundException)
async def registry_not_found_handler(request: Request, exc: RegistryNotFoundException):
    return JSONResponse(content=exc.msg, status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(InvalidOperationException)
async def invalid_operation_handler(request: Request, exc: InvalidOperationException):
    return JSONResponse(content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(NonPositiveTransactionValueException)
async def non_positive_transaction_value_handler(
    request: Request, exc: NonPositiveTransactionValueException
):
    return JSONResponse(content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(InsufficientBalanceException)
async def insufficient_balance_handler(
    request: Request, exc: InsufficientBalanceException
):
    return JSONResponse(content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(BankIntegrityFailException)
async def integrity_error_handler(request: Request, exc: BankIntegrityFailException):
    return JSONResponse(content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(ExceedUserAccountsException)
async def exceed_user_accounts(request: Request, exc: ExceedUserAccountsException):
    return JSONResponse(
        content=exc.msg, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.exception_handler(CredentialsTokenException)
async def credentials_token_handler(request: Request, exc: CredentialsTokenException):
    return JSONResponse(
        content=exc.msg,
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={'WWW-Authenticate': 'Bearer'},
    )


@app.exception_handler(UsernameAuthenticationFailException)
async def username_authentication_handler(
    request: Request, exc: UsernameAuthenticationFailException
):
    return JSONResponse(
        content=exc.msg,
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={'WWW-Authenticate': 'Bearer'},
    )


@app.exception_handler(PasswordAuthenticationFailException)
async def password_authentication_handler(
    request: Request, exc: PasswordAuthenticationFailException
):
    return JSONResponse(
        content=exc.msg,
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={'WWW-Authenticate': 'Bearer'},
    )
