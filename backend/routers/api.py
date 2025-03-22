import uuid
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from crud import DBController
from models import APIKey,HTTPMethodEnum, APIUsage


router = APIRouter()


class GenerateAPIKeyRequest(BaseModel):
    id: int

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
    result = None
    for _ in range(5):
        try:
            new_key = create_api_key()
            key_exist = dbController.is_key_already_exist(new_key)

            if key_exist:
                continue

            result = await dbController.insert_data(
                    APIKey, user_id=user_id, key=new_key
                    )
            if result and result.get("success"):
                api_key_id = dbController.get_api_key_by_user_id(user_id)
                if api_key_id:
                    for method in HTTPMethodEnum:
                        await dbController.insert_data(APIUsage,key_id=api_key_id, count=0, method=method.value)

                    return {
                        "success": True,
                        "message": "Your API key generated successfully.",
                        "key": new_key,
                        "id": user_id
                    }
                else:
                    return {
                        "success": False,
                        "message": "Your API key could not be generated.",
                        "key": new_key,
                        "id": user_id
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
        "id": user_id
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


def main():
    pass


if __name__ == "__main__":
    main()
