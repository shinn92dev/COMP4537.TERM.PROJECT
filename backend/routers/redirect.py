from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from utils.jwt_handler import check_is_admin

router = APIRouter()


@router.get("/redirect-check", response_model=bool | None)
async def redirect_check(
    is_admin: Annotated[bool | None, Depends(check_is_admin)]
):
    return is_admin


def main():
    pass


if __name__ == "__main__":
    main()
