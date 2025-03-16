from fastapi import APIRouter, Depends
from typing import Annotated
from utils.jwt_handler import get_current_user
from schemas import User


router = APIRouter()


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


def main():
    pass


if __name__ == "__main__":
    main()
