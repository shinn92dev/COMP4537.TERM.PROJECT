from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from utils.auth import authenticate_user
from utils.jwt_handler import create_access_token
from datetime import timedelta
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from utils.govee import Govee
load_dotenv()

ENV = os.getenv("ENV", "development")

router = APIRouter()

class APIKeyRequest(BaseModel):
    goveeKey: str


@router.post("/get-devices")
async def get_devices(payload: APIKeyRequest):
    govee_key = payload.goveeKey
    goveeController = Govee(govee_key)
    devices = goveeController.get_govee_devices()
    if devices:
        return {"success": True,  "message": "Devices fected successfully.", "data": {"devices": devices}}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fetching devices fail",
            headers={"WWW-Authenticate": "Bearer"}
        )

class GoveeControlRequest(BaseModel):
    goveeKey: str
    device: dict
    isOn: bool


@router.post("/turn-on-off")
async def turn_on_and_off(payload: GoveeControlRequest):
    govee_key = payload.goveeKey
    device = payload.device
    is_on = payload.isOn
    goveeController = Govee(govee_key)
    goveeController.turn_on_and_off(device, is_on)
    print(is_on)


class GoveeControlRequest(BaseModel):
    goveeKey: str
    device: dict
    color: dict


@router.post("/set-color")
async dev set_color(payload: GoveeControlRequest):
    govee_key = payload.goveeKey
    device = payload.device
    color = payload.color
    goveeController = Govee(govee_key)
    goveeController.set_color(device, color)



@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
        ):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    ACCESS_TOKEN_EXPIRE_MINUTES = 180
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id), "is_admin": user.is_admin}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="None",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"message": "Login successful. Cookie is set.", "is_admin": user.is_admin, "success": True}