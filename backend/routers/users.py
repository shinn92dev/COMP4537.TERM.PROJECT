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
    print("[/me] Current user fetched successfully:")
    print("User ID:", current_user.user_id)
    print("Username:", current_user.username)
    print("Is Admin:", current_user.is_admin)
    return current_user


def require_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get("user")

        print("[/admin] Checking admin privileges...")
        if not user:
            print("→ No user found in kwargs")
            raise HTTPException(status_code=403, detail="Admin access required")

        print("User ID:", user.user_id)
        print("Is Admin:", user.is_admin)

        if not getattr(user, "is_admin", False):
            print("→ User is not admin")
            raise HTTPException(status_code=403, detail="Admin access required")

        print("→ User is admin. Access granted.")
        return await func(*args, **kwargs)
    return wrapper


@router.get("/admin")
@require_admin
async def admin_page(user=Annotated[User, Depends(get_current_user)]):
    print("[/admin] Admin endpoint reached")
    return user


def main():
    pass


if __name__ == "__main__":
    main()
