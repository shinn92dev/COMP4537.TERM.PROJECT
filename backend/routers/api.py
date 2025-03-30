import uuid
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from crud import DBController
from models import APIKey, HTTPMethodEnum, APIUsage
import traceback


router = APIRouter()


class GenerateAPIKeyRequest(BaseModel):
    id: int
    key_name: str


class GenerateAPIKeyResponse(GenerateAPIKeyRequest):
    success: bool
    message: str
    key: str


dbController = DBController()


def create_api_key():
    return str(uuid.uuid4())


@router.post("/generate", response_model=GenerateAPIKeyResponse)
async def generate_api_key(body: GenerateAPIKeyRequest):
    user_id = body.id
    key_name = body.key_name
    active = True
    result = None
    for _ in range(5):
        try:
            new_key = create_api_key()
            key_exist = dbController.is_key_already_exist(new_key)

            if key_exist:
                continue

            result = await dbController.insert_data(
                APIKey, user_id=user_id, key=new_key, key_name=key_name, active=active
                    )
            if result and result.get("success"):
                api_key_id = dbController.get_api_key_by_user_id(user_id)
                if api_key_id:
                    for method in HTTPMethodEnum:
                        await dbController.insert_data(
                            APIUsage,
                            key_id=api_key_id,
                            count=0,
                            method=method.value,
                            endpoint=None
                            )

                    return {
                        "success": True,
                        "message": "Your API key generated successfully.",
                        "key": new_key,
                        "id": user_id,
                        "key_name": key_name,
                    }
                else:
                    return {
                        "success": False,
                        "message": "Your API key could not be generated.",
                        "key": new_key,
                        "id": user_id,
                        "key_name": key_name,
                    }

            elif result and not result.get("success"):
                raise Exception(result.get("message"))
        except Exception as e:
            print(f"Error in attempt: {str(e)}")
    return {
        "success": False,
        "error": "Exception",
        "message":
        "Failed to generate a unique API Key after multiple attempts.",
        "key":"",
        "id": user_id,
        "key_name": key_name,
    }


class DeleteAPIKeyRequest(BaseModel):
    user_id: int


@router.get("/get-key")
def get_api_key(user_id: int):
    api_keys = dbController.get_all_api_keys_for_a_user(user_id)
    if not api_keys:
        raise HTTPException(
            status_code=404, detail="API key not found for this user."
            )
    return {"success": True, "keys": api_keys}


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


class UpdateAPIKeyActivation(BaseModel):
    user_id: int
    key: str
    current_status: str


@router.patch("/update-key-activation")
async def update_key_activation(body: UpdateAPIKeyActivation):
    print(f"id: {body.user_id}")
    print(f"key: {body.key}")
    print(f"current_status: {body.current_status}")
    if not body.user_id:
        raise HTTPException(
            status_code=400, detail="User ID is required in the header."
        )
    if not body.key:
        raise HTTPException(
            status_code=400, detail="Key is required in the header."
        )
    if not dbController.is_valid_api_key(body.key):
        raise HTTPException(
            status_code=403, detail="Invalid API Key for this user."
        )
    api_key = body.key
    status_mapping = {
        "active": False,
        "inactive": True
    }
    update_status_to = status_mapping.get(body.current_status)
    if update_status_to is None:
        raise HTTPException(
            status_code=400, detail="Invalid status code."
        )
    try:
        update_result = dbController.update_api_key_activation(api_key, update_status_to)
        if update_result.get("success"):
            return {
                "success": True,
                "message": f"Your API key's activation was successful set to {update_status_to}.",
            }
        else:
            return {
                "success": False,
                "message": f"Your API key's activation was not successful set to {update_status_to}.",
            }
    except Exception as e:
        print(f"Error in update_key_activation: {str(e)}")
        print(traceback.format_exc())  # 打印完整错误堆栈
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the request.")


def main():
    pass


if __name__ == "__main__":
    main()
