from fastapi import APIRouter, HTTPException, Depends, status
from backend.utils.ai_rag import ask_to_ai_rag
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
    try:
        govee_key = payload.goveeKey
        if not govee_key:
            raise HTTPException(status_code=400, detail="Missing Govee API key.")
        goveeController = Govee(govee_key)
        devices = goveeController.get_govee_devices()

        if not devices:
            raise HTTPException(status_code=404, detail="No devices found for the given key.")

        return {
            "success": True,
            "message": "Devices fetched successfully.",
            "data": {"devices": devices}
        }
    except Exception as e:
        print("❌ Error in get-devices:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch devices.")


class GoveeControlRequest(BaseModel):
    goveeKey: str
    device: dict
    isOn: bool


@router.post("/turn-on-off")
async def turn_on_and_off(payload: GoveeControlRequest):
    try:
        goveeController = Govee(payload.goveeKey)
        result = goveeController.turn_on_and_off(payload.device, payload.isOn)
        if not result:
            raise HTTPException(status_code=400, detail="Failed to change power state.")
        return {"message": "Device state updated."}
    except Exception as e:
        print("❌ Error in turn-on-off:", e)
        raise HTTPException(status_code=500, detail="Failed to change device power state.")


class GoveeColorControlRequest(BaseModel):
    goveeKey: str
    device: dict
    color: dict


@router.post("/set-color")
async def set_color(payload: GoveeColorControlRequest):
    try:
        goveeController = Govee(payload.goveeKey)
        result = goveeController.set_lamp_color(payload.device, payload.color)
        if not result:
            raise HTTPException(status_code=400, detail="Failed to update color.")
        return {"message": "Color updated successfully."}
    except Exception as e:
        print("❌ Error in set-color:", e)
        raise HTTPException(status_code=500, detail="Failed to set color.")


class GoveeBrightnessControlRequest(BaseModel):
    goveeKey: str
    device: dict
    brightness: int


@router.post("/set-brightness")
async def set_brightness(payload: GoveeBrightnessControlRequest):
    try:
        if payload.brightness < 1 or payload.brightness > 100:
            raise HTTPException(status_code=400, detail="Brightness must be between 1 and 100.")
        goveeController = Govee(payload.goveeKey)
        result = goveeController.set_lamp_brightness(payload.device, payload.brightness)
        if not result:
            raise HTTPException(status_code=400, detail="Failed to update brightness.")
        return {"message": "Brightness updated successfully."}
    except Exception as e:
        print("❌ Error in set-brightness:", e)
        raise HTTPException(status_code=500, detail="Failed to set brightness.")


class GoveeAIControlRequest(BaseModel):
    goveeKey: str
    device: dict
    emotion: str
    time: str
    addReq: str | None = None



def hex_to_rgb(hex_code: str) -> dict:
    hex_code = hex_code.lstrip('#')

    if len(hex_code) == 3:
        hex_code = ''.join([c * 2 for c in hex_code])

    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)

    return {"r": r, "g": g, "b": b}


@router.post("/set-color-by-ai")
async def set_color_by_ai(payload: GoveeAIControlRequest):
    try:
        if not payload.emotion:
            raise HTTPException(status_code=400, detail="Emotion is required.")
        if not payload.time:
            raise HTTPException(status_code=400, detail="Time is required.")

        prompt_parts = [f"Emotion: {payload.emotion}", f"Time: {payload.time}"]
        if payload.addReq:
            prompt_parts.append(f"Request: {payload.addReq}")
        prompt = ", ".join(prompt_parts)

        answer = ask_to_ai_rag(prompt)
        if "color" not in answer:
            raise HTTPException(status_code=422, detail="AI failed to return a valid color.")

        rgb_color = hex_to_rgb(answer["color"])
        govee_controller = Govee(payload.goveeKey)
        govee_controller.set_lamp_color(payload.device, rgb_color)

        return {
            "status": "success",
            "message": "AI color suggestion applied.",
            "prompt": prompt,
            "data": answer,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print("❌ Unexpected error:", e)
        raise HTTPException(status_code=500, detail="Internal server error.")
    