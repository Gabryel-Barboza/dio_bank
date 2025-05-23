# Exceção para registros não encontrados
class RegistryNotFoundException(Exception):
    """Raised when a registry is not found in the database."""

    def __init__(self, msg: str = None):
        self.msg = {'detail': msg or 'Registry not found! Aborting operation...'}


# Exceção para usuário inválido na criação de contas
class UserNotFoundException(Exception):
    """Raised when an account is created without an existent user."""

    def __init__(self, msg: str = None):
        self.msg = {'detail': msg or 'User not found! Aborting operation...'}


# Exceção para limite máximo de contas por usuário
class ExceedUserAccountsException(Exception):
    """Raised when the maximum account limit is exceeded for an user."""

    def __init__(self, limit: int, msg: str = None):
        self.msg = {
            'detail': msg
            or f'User accounts exceeded the maximum of {limit}! Aborting operation...'
        }


# Exceção para tipo de transação inválida escolhida
class InvalidOperationException(Exception):
    """Raised when an invalid transaction type is received."""

    def __init__(self, msg: str = None):
        self.msg = {'detail': msg or 'Invalid operation selected! Please try again...'}


# Exceção para valor de transação não positivo
class NonPositiveTransactionValueException(Exception):
    """Raised when a value less than or equal to zero is received in a transaction."""

    def __init__(self, msg: str = None):
        self.msg = {
            'detail': msg
            or 'Invalid transaction value received, minimum value must be greater than zero!'
        }


# Exceção para saldo insuficiente para saque
class InsufficientBalanceException(Exception):
    """Raised when the selected account doesn't have sufficient balance to finish a withdraw."""

    def __init__(self, msg: str = None):
        self.msg = {'detail': msg or 'Insufficient balance to finish the operation!'}


# Exceção para falha na autenticação com usuário
class UsernameAuthenticationFailException(Exception):
    """Raised when an user tries to authenticate with an invalid username, that is, it is not found in the database."""

    def __init__(self, msg: str = None):
        self.msg = {
            'detail': msg or "Invalid username inserted or it doesn't exist, try again!"
        }


# Exceção para falha na autenticação com senha
class PasswordAuthenticationFailException(Exception):
    """Raised when an user tries to authenticate with an invalid password."""

    def __init__(self, msg: str = None):
        self.msg = {'detail': msg or 'Invalid password inserted, try again!'}


# Exceção para token de acesso inválido
class CredentialsTokenException(Exception):
    """Raised when an invalid access token is used to authenticate."""

    def __init__(self, msg: str = None):
        self.msg = {
            'detail': msg
            or 'Invalid authentication token, please signin to your user again!'
        }


# Exceção para erros de integridade com o banco
class BankIntegrityFailException(Exception):
    """Raised when an integrity error from SQLAlchemy occurs."""

    def __init__(self, msg: str = None, constr_error: str = 'Unidentified'):
        self.msg = {
            'detail': msg
            or 'An integrity error occurred with the registry received! Aborting operation...',
            'failed_at': constr_error,
        }
