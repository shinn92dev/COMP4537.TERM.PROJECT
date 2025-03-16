from fastapi import APIRouter, Depends
from utils.jwt_handler import get_current_user
from schemas import UserDashboardResponse

router = APIRouter()

@router.get("/user-info", response_model=UserDashboardResponse)
async def get_user_info(current_user: dict = Depends(get_current_user)):
    return {
        # "name": current_user["username"],
        # "email": current_user["email"],
        # "requestLimit": current_user["request_limit"],
        # "remainingRequests": current_user["remaining_requests"]
        "name": "Test User",
        "email": "testuser@test.com",
        "requestLimit": 20,
        "remainingRequests": 10
    }