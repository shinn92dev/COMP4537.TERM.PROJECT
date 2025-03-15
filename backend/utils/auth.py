import bcrypt
from backend.crud import get_user
from backend.models import User


def hash_password(password: str) -> str:
    encoded_password = password.encode()
    salt_round = 10
    salt = bcrypt.gensalt(salt_round)
    return bcrypt.hashpw(encoded_password, salt).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    encoded_password = password.encode()
    encoded_hashed_password = hashed_password.encode()
    return bcrypt.checkpw(encoded_password, encoded_hashed_password)


def authenticate_user(db, email: int, password: str) -> User | bool:
    user = get_user(db, email)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def main():
    password = "Hello_World.123"
    hashed_password = hash_password(password)
    print(verify_password(password, hashed_password))


if __name__ == '__main__':
    main()
