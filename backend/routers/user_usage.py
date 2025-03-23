from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from utils.jwt_handler import get_current_user
from schemas import User
from sqlalchemy.orm import Session
from crud import get_db
from sqlalchemy import func
from models import APIKey, APIUsage

router = APIRouter()

@router.get("/usage")
async def get_user_usage(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)):

    user_keys = db.query(APIKey).filter_by(user_id=current_user.user_id).all()

    if not user_keys:
        return {
            "request_limit": 20,
            "total_used": 0,
            "remaining_requests": 20
        }
    
    key_ids = [k.key_id for k in user_keys]
    
    total_used = (
        db.query(func.sum(APIUsage.count))
        .filter(APIUsage.key_id.in_(key_ids))
        .scalar()
    )
    total_used = total_used or 0

    request_limit = 20
    remaining = request_limit - total_used

    return {
        "request_limit":request_limit,
        "total_used": total_used,
        "remaining_requests": max(remaining, 0)
    }