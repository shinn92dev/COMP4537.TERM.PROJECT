import uuid
from fastapi import APIRouter, HTTPException, Header, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from crud import DBController
from models import APIKey
from typing import Annotated
from utils.auth import authenticate_user
from utils.jwt_handler import create_access_token, get_current_user
from datetime import timedelta
from schemas import Token, User


router = APIRouter()


class GenerateAPIKeyRequest(BaseModel):
    id: int


dbController = DBController()


@router.post("/generate", response_model=GenerateAPIKeyRequest)
def generate_api_key(body: GenerateAPIKeyRequest):
    user_id = body.id
    result = None
    for _ in range(5):
        try:
            new_key = str(uuid.uuid4())
            key_exist = dbController.is_key_already_exist(new_key)
            if not key_exist:
                result = dbController.insert_data(
                    APIKey, id=user_id, key=new_key
                    )
                if result and result.get("success", None):
                    return {
                        "success": True,
                        "message": "Your API key generated successfully.",
                        "key": new_key
                    }
                elif result and not result.get("success", True):
                    raise Exception(result.get("message"))
        except Exception as e:
            return {
                "success": False,
                "error": "Exception",
                "message": str(e)
            }
    return {
        "success": False,
        "error": "Exception",
        "message":
        "Failed to generate a unique API Key after multiple attempts."
    }


class DeleteAPIKeyRequest(BaseModel):
    user_id: int


@router.get("/get-key")
def get_api_key(user_id: int):
    api_key = dbController.get_api_key_by_user_id(user_id)
    if not api_key:
        raise HTTPException(
            status_code=404, detail="API key not found for this user."
            )
    return {"success": True, "key": api_key}


@router.delete("/delete-key")
def delete_api_key(body: DeleteAPIKeyRequest, api_key: str = Header(None)):
    if not api_key:
        raise HTTPException(
            status_code=400, detail="API Key is required in the header."
            )
    is_valid_key = dbController.is_valid_api_key(api_key)
    if not is_valid_key:
        raise HTTPException(
            status_code=403, detail="Invalid API Key for this user."
            )
    result = dbController.delete_api_key(body.user_id, api_key)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Matching API Key not found for this user to delete."
            )
    return {"success": True, "message": "API Key deleted successfully."}


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.email, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


def main():
    pass


if __name__ == "__main__":
    main()
