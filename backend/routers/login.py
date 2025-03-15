from fastapi import APIRouter, HTTPException, Header, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from utils.auth import authenticate_user
from utils.jwt_handler import create_access_token, get_current_user
from datetime import timedelta
from schemas import Token, User


router = APIRouter()


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.email, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


def main():
    pass


if __name__ == "__main__":
    main()
