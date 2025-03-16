from fastapi import APIRouter
from crud import DBController
from models import User
from pydantic import BaseModel
from utils import auth

dbController = DBController()

router = APIRouter()


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register")
async def register(user_info: UserRegister):
    username = user_info.username
    email = user_info.email
    hashed_password = auth.hash_password(user_info.password)

    print(f"DATA Received | user_name: {username}, email: {email}.")
    response = await dbController.insert_data(
        User,
        name=username,
        email=email,
        password=hashed_password,
        is_admin=False
    )
    print(f"RESPONSE from the server: {response}")
    if response["success"]:
        return {"message": response["message"]}

    return {"message": response["error"]}
