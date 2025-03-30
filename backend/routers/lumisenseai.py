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
import requests
import json

load_dotenv()
OLLAMA_URL = "http://localhost:11434/api/generate"

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


class GoveeColorControlRequest(BaseModel):
    goveeKey: str
    device: dict
    color: dict


@router.post("/set-color")
async def set_color(payload: GoveeColorControlRequest):
    govee_key = payload.goveeKey
    device = payload.device
    color = payload.color
    goveeController = Govee(govee_key)
    goveeController.set_lamp_color(device, color)


class GoveeBrightnessControlRequest(BaseModel):
    goveeKey: str
    device: dict
    brightness: int


@router.post("/set-brightness")
async def set_brightness(payload: GoveeBrightnessControlRequest):
    govee_key = payload.goveeKey
    device = payload.device
    brightness = payload.brightness
    goveeController = Govee(govee_key)
    goveeController.set_lamp_brightness(device, brightness)


class GoveeAIControlRequest(BaseModel):
    goveeKey: str
    device: dict
    emotion: str
    time: str
    addReq: str | None = None


def ask_to_ai(prompt: str):
    try:
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=6000)

        if response.status_code == 200:
            result = response.json().get("response", "")
            print("RESULT BEFORE FORMATTING: ", result)

            try:
                final_result = json.loads(result)
                print("RESULT AFTER FORMATTING: ", final_result)
                return final_result
            except json.JSONDecodeError as e:
                print("❌ JSON Parsing Error:", e)
                raise HTTPException(
                    status_code=500,
                    detail="AI response format is invalid"
                )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to generate response from AI"
            )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to AI server"
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=500,
            detail="AI server timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected server error: {e}"
        )


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
        govee_key = payload.goveeKey
        device = payload.device
        emotion = payload.emotion
        time = payload.time
        add_req = payload.addReq

        if not emotion:
            raise HTTPException(status_code=400, detail="Emotion is required.")

        prompt_parts = [f"Emotion: {emotion}"]

        if time:
            prompt_parts.append(f"Time: {time}")
        if add_req:
            prompt_parts.append(f"Additional Request: {add_req}")

        prompt = ", ".join(prompt_parts)
        prompt += (
            ". Based on this, recommend a light color in HEX, "
            "reason, and one piece of advice."
        )
        prompt += (
            " Format the answer in JSON format like this: "
            "{\"color\": \"answer\", \"reason\": \"reason\", "
            "\"advice\": \"advice\"}"
        )

        answer = ask_to_ai(prompt)
        govee_controller = Govee(govee_key)
        govee_controller.set_lamp_color(device, hex_to_rgb(answer["color"]))
        return {
            "status": "success",
            "message": "Request processed successfully.",
            "prompt": prompt,
            "data": answer,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print("❌ Unexpected error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
