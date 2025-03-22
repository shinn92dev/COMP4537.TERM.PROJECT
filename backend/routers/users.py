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


def require_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get("user")

        if not user or not getattr(user, "is_admin", False):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        return await func(*args, **kwargs)
    return wrapper


@router.get("/admin")
@require_admin
async def admin_page(user=Annotated[User, Depends(get_current_user)]):
    return user


def main():
    pass


if __name__ == "__main__":
    main()
