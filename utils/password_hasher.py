from passlib.context import CryptContext

password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)
