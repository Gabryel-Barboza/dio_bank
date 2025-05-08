from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

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


# Classe para sobrescrever o padrão do starlette e criar um middleware para tratar exceções
class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    # Deve sobrescrever o método dispatch da classe original
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)

            return response
        except RegistryNotFoundException as exc:
            return JSONResponse(content=exc.msg, status_code=status.HTTP_404_NOT_FOUND)
        except UserNotFoundException as exc:
            return JSONResponse(
                content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST
            )
        except InvalidOperationException as exc:
            return JSONResponse(
                content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST
            )
        except NonPositiveTransactionValueException as exc:
            return JSONResponse(
                content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST
            )
        except InsufficientBalanceException as exc:
            return JSONResponse(
                content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST
            )
        except BankIntegrityFailException as exc:
            return JSONResponse(
                content=exc.msg, status_code=status.HTTP_400_BAD_REQUEST
            )
        except ExceedUserAccountsException as exc:
            return JSONResponse(
                content=exc.msg, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except CredentialsTokenException as exc:
            return JSONResponse(
                content=exc.msg,
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={'WWW-Authenticate': 'Bearer'},
            )
        except UsernameAuthenticationFailException as exc:
            return JSONResponse(
                content=exc.msg,
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={'WWW-Authenticate': 'Bearer'},
            )
        except PasswordAuthenticationFailException as exc:
            return JSONResponse(
                content=exc.msg,
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={'WWW-Authenticate': 'Bearer'},
            )
