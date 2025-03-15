from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import jwt
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.crud import get_user
from backend.schemas import TokenData

load_dotenv("../.env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


if not SECRET_KEY:
    raise ValueError("SESSION_KEY is not set! Please configure it in .env or environment variables.")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise credential_exception
        token_data = TokenData(id=user_id)

    except InvalidTokenError:
        raise credential_exception

    user = get_user(db, token_data.id)

    if not user:
        raise credential_exception

    return user


def main():
    pass


if __name__ == '__main__':
    main()
