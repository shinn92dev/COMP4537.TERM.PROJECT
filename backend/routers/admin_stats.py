from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from utils.jwt_handler import get_current_user
from schemas import User
from crud import DBController
from models import APIUsage, HTTPMethodEnum
from sqlalchemy import func

router = APIRouter()
db_controller = DBController()

@router.get("/endpoint-breakdown")
async def get_endpoint_breakdown(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(db_controller.get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized as admin."
        )
    
    results = (
        db.query(
            APIUsage.method.label("method"),
            APIUsage.endpoint.label("endpoint"),
            func.sum(APIUsage.count).label("total_requests")
        )
        .group_by(APIUsage.method, APIUsage.endpoint)
        .all()
    )

    data = []
    for row in results:
        method_str = row.method.value if isinstance(row.method, HTTPMethodEnum) else row.method
        data.append({
            "method": method_str,
            "endpoint": row.endpoint or "",
            "totalRequests": row.total_requests or 0
        })
    return {"data": data}
