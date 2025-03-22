from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import jwt
# from typing import Annotated
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from crud import DBController
from schemas import TokenData

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

print(SECRET_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


if not SECRET_KEY:
    raise ValueError(
        "SESSION_KEY is not set! Please configure it in .env "
        "or environment variables."
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get("access_token")
    if not token:
        raise credential_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        print(f"\nuser_id: {user_id}")
        is_admin = payload.get("is_admin")
        print(f"\nis_admin: {is_admin}")
        print(is_admin)
        if not user_id:
            raise credential_exception
        token_data = TokenData(user_id=user_id)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except InvalidTokenError:
        print("\nfail to decode")

        raise credential_exception

    user = DBController.fetch_user_by_user_id(token_data.user_id)
    if not user:
        raise credential_exception

    return user


def main():
    pass


if __name__ == '__main__':
    main()
