import json
import requests
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()


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


class ColorRequest(BaseModel):
    weather: str | None = None
    emotion: str
    location: str | None = None
    time: str
    add_req: str | None = None


@router.post("/recommend-color/")
async def return_ai_answer(request: ColorRequest):
    try:
        weather = request.weather
        emotion = request.emotion
        location = request.location
        time = request.time
        add_req = request.add_req

        if not emotion:
            raise HTTPException(status_code=400, detail="Emotion is required.")

        prompt_parts = [f"Emotion: {emotion}"]
        if weather:
            prompt_parts.append(f"Weather: {weather}")
        if location:
            prompt_parts.append(f"Location: {location}")
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

        return {
            "status": "success",
            "message": "Request processed successfully.",
            "prompt": prompt,
            "data": answer,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print("❌ Unexpected error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


def main():
    prompt = (
        "emotion: happy, weather: rainy, location: vancouver, "
        "time: 6:49. Based on this, recommend color for light "
        "in HEX, reason, and the one advice. Format the answer "
        "in JSON format like this: {'color': answer, 'reason': "
        "reason, 'advice': advice}"
    )
    answer = ask_to_ai(prompt)
    print(answer)


if __name__ == "__main__":
    main()
