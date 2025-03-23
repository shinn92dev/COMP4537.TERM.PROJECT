from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from utils.jwt_handler import get_current_user
from schemas import User

router = APIRouter()

@router.get("/usage")
async def get_user_usage(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.request_limit is None or current_user.total_requests_used is None:
        raise HTTPException(status_code=400, detail="Usage data not found for this user")
    
    remaining = current_user.request_limit - current_user.total_requests_used

    return {
        "request_limit": current_user.request_limit,
        "total_used": current_user.total_requests_used,
        "remaining_requests": remaining
    }