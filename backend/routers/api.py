import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from crud import DBController
from models import APIKey


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


@router.get("/get-key")
def get_api_key(user_id: int):
    api_key = dbController.get_api_key_by_user_id(user_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found for this user.")
    return {"success": True, "key": api_key}


def main():
    api_key = str(uuid.uuid4())
    print(api_key)


if __name__ == "__main__":
    main()
