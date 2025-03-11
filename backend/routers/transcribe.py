from fastapi import APIRouter
# File, UploadFile
import vosk
# import wave
# import json
import os

router = APIRouter()

# Loading vosk model for audio to text generation
MODEL_PATH = "../ai_models/vosk-model-small-en-us-0.15"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("❌ Vosk cannot be found.")
else:
    print("✅ Vosk loaded successfully.")

model = vosk.Model(MODEL_PATH)
