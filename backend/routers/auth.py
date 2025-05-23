from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from utils.auth import authenticate_user
from utils.jwt_handler import create_access_token
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV", "development")

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
        ):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    ACCESS_TOKEN_EXPIRE_MINUTES = 180
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id), "is_admin": user.is_admin}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="None",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"message": "Login successful. Cookie is set.", "is_admin": user.is_admin, "success": True}


@router.delete("/token")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="None",
    )
    return {"message": "Logged out successfully", "success": True}


def main():
    pass


if __name__ == "__main__":
    main()
