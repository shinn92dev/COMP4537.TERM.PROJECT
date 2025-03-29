from fastapi import APIRouter, Depends, HTTPException
# from typing import List
from utils.jwt_handler import get_current_user
from schemas import User
from sqlalchemy.orm import Session
from crud import DBController
from sqlalchemy import func
from models import User as UserModel, APIKey, APIUsage

router = APIRouter()
db_controller = DBController()


@router.get("/user-breakdown")
async def get_user_breakdown(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(db_controller.get_db),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized as admin.")

    results = (
        db.query(
            UserModel.username.label("username"),
            UserModel.email.label("email"),
            func.group_concat(APIKey.key).label("keys"),
            func.sum(APIUsage.count).label("total_requests")
        )
        .join(APIKey, UserModel.user_id == APIKey.user_id, isouter=True)
        .join(APIUsage, APIKey.key_id == APIUsage.key_id, isouter=True)
        .group_by(UserModel.user_id, UserModel.username, UserModel.email)
        .all()
    )

    data = []
    for row in results:
        data.append({
            "username": row.username,
            "email": row.email,
            "token": (row.keys.split(",") if row.keys else []),
            "totalRequests": row.total_requests or 0
        })
    return {"data": data}
