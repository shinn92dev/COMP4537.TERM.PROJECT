from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from utils.auth import authenticate_user
from utils.jwt_handler import create_access_token
from dotenv import load_dotenv
from pydantic import BaseModel
from utils.govee import Govee
import requests
import json
OLLAMA_URL = "http://localhost:11434/api/generate"

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
