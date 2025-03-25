class RegistryNotFoundException(Exception):
    """Raised when a registry is not found in the database."""

    def __init__(self):
        self.msg = 'Registry not found! Aborting operation...'


class UsernameAuthenticationFailException(Exception):
    """Raised when an user tries to authenticate with an invalid username, that is, it is not found in the database."""

    def __init__(self):
        self.msg = 'Invalid username inserted, try again!'


class PasswordAuthenticationFailException(Exception):
    """Raised when an user tries to authenticate with an invalid password."""

    def __init__(self):
        self.msg = 'Invalid password inserted, try again!'
