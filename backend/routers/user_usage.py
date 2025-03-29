from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from utils.jwt_handler import get_current_user_id
from sqlalchemy.orm import Session
from crud import DBController
from sqlalchemy import func
from models import APIKey, APIUsage

router = APIRouter()
db_controller = DBController()

@router.get("/usage")
async def get_user_usage(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Session = Depends(db_controller.get_db)):

    user_keys = db.query(APIKey).filter_by(user_id=user_id).all()

    print(f"user id = {user_id}")

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