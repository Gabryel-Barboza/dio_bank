class RegistryNotFoundException(Exception):
    """Raised when a registry is not found in the database."""

    def __init__(self):
        self.msg = 'Registry not found! Aborting operation...'
