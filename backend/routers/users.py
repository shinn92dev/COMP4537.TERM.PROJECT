from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from utils.jwt_handler import get_current_user
from schemas import User
from functools import wraps

router = APIRouter()


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


async def get_admin_user(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return user


@router.get("/admin", response_model=User)

async def admin_page(user=Annotated[User, Depends(get_admin_user)]):
    return user


def main():
    pass


if __name__ == "__main__":
    main()
