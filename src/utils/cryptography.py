from passlib.context import CryptContext

passwd_hash = CryptContext(schemes=['pbkdf2_sha256'])


# Função para criar hash de senhas
def hash_password(password: str) -> dict:
    """Receives a password and hashes it with the default hash algorithm.

    Default=pbkdf2_sha256.

    :return: dict={'password': hashed_password}"""
    password = str.encode(password)
    hashed_password = {'password': (passwd_hash.hash(password))}

    return hashed_password


def verify_hash(password: str, hashed_password: str) -> bool:
    """Validate the password received by applying the default hash algorithm and comparing to the hashed password."""
    return passwd_hash.verify(password, hashed_password)
