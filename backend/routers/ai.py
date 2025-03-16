import json
import requests
import datetime
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_to_ai(prompt: str):
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        result = response.json()["response"]
        print("RESULT BEFORE FORMATTING: ", result)
        try:
            final_result = json.loads(result)
            print("RESULT AFTER FORMATTING: ", final_result)
            return final_result
        except Exception as e:
            print(e)
            return {"error": f"Failed to generate response {e}"}
    else:
        return {"error": "Failed to generate response"}


class ColorRequest(BaseModel):
    weather: str | None = None
    emotion: str
    location: str | None = None
    time: str
    add_req: str | None = None


@router.post("/recommend-color/")
async def return_ai_answer(request: ColorRequest):
    weather = request.weather
    emotion = request.emotion
    location = request.location
    time = request.time
    add_req = request.add_req
    prompt_parts = [f"Emotion: {emotion}"]
    if not emotion:
        print("❌Emotion is required.")
        return None
    if weather:
        {prompt_parts.append(f"Weather: {weather}")}
    if location:
        prompt_parts.append(f"Location: {location}")
    if time:
        prompt_parts.append(f"Time: {time}")
    if add_req:
        prompt_parts.append(f"Additional Request: {add_req}")

    prompt = ", ".join(prompt_parts) 
    prompt += ". Based on this, recommend a light color in HEX, reason, and one piece of advice."
    prompt += " Format the answer in JSON format like this: {\"color\": \"answer\", \"reason\": \"reason\", \"advice\": \"advice\"}"
    answer = ask_to_ai(prompt)
    return {
        "status": "success",
        "message": "Request processed successfully.",
        "prompt": prompt,
        "data": answer,
        "timestamp": datetime.now()
    }


def main():
    prompt = "emotion: happy, weather: rainy, location: vancouver, time: 6:49. Based on this, recommend color for light in HEX, reason, and the one advice. Format the answer in JSON format like this. {{'color': answer, 'reason': reason, 'advice': advice}}"
    answer = ask_to_ai(prompt)
    print(answer)


if __name__ == "__main__":
    main()
