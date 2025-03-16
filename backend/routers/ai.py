import os
from fastapi import APIRouter
from transformers import AutoTokenizer, AutoModelForCausalLM
import requests
import json

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
        try:
            final_result = json.loads(result)
            return final_result
        except Exception as e:
            return {"error": f"Failed to generate response {e}"}
    else:
        return {"error": "Failed to generate response"}


@router.get("/")
def return_ai_answer(prompt: str = None):
    answer = ask_to_ai(prompt)
    return {
        "prompt": prompt,
        "result": answer
    }


def main():
    prompt = "emotion: happy, weather: rainy, location: vancouver, time: 6:49. Based on this, recommend color for light in HEX, reason, and the one advice. Format the answer in JSON format like this. {{'color': answer, 'reason': reason, 'advice': advice}}"
    answer = ask_to_ai(prompt)
    print(answer)


if __name__ == "__main__":
    main()
