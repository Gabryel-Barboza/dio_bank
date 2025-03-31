# Exceção para registros não encontrados
class RegistryNotFoundException(Exception):
    """Raised when a registry is not found in the database."""

    def __init__(self):
        self.msg = 'Registry not found! Aborting operation...'


# Exceção para usuário inválido na criação de contas
class UserNotFoundException(Exception):
    """Raised when an account is created without an existent user."""

    def __init__(self):
        self.msg = 'User not found! Aborting operation...'


# Exceção para limite máximo de contas por usuário
class ExceedUserAccountsException(Exception):
    """Raised when the maximum account limit is exceeded for an user."""

    def __init__(self, limit: int):
        self.msg = (
            f'User accounts exceeded the maximum of {limit}! Aborting operation...'
        )


# Exceção para tipo de transação inválida escolhida
class InvalidOperationException(Exception):
    """Raised when an invalid transaction type is received."""

    def __init__(self):
        self.msg = 'Invalid operation selected! Please try again...'


# Exceção para saldo insuficiente para saque
class InsufficientBalanceException(Exception):
    """Raised when the selected account doesn't have sufficient balance to finish a withdraw."""

    def __init__(self):
        self.msg = 'Insufficient balance to finish the operation!'


# Exceção para falha na autenticação com usuário
class UsernameAuthenticationFailException(Exception):
    """Raised when an user tries to authenticate with an invalid username, that is, it is not found in the database."""

    def __init__(self):
        self.msg = 'Invalid username inserted, try again!'


# Exceção para falha na autenticação com senha
class PasswordAuthenticationFailException(Exception):
    """Raised when an user tries to authenticate with an invalid password."""

    def __init__(self):
        self.msg = 'Invalid password inserted, try again!'


# Exceção para token de acesso inválido
class CredentialsTokenException(Exception):
    """Raised when an invalid access token is used to authenticate."""

    def __init__(self):
        self.msg = 'Invalid authentication token, please signin to your user again!'
