import os
from fastapi import APIRouter
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


router = APIRouter()

# Load Googld FLAN-T5 Model
model_path = os.path.abspath("../ai_models")
os.environ["HUGGINGFACE_HUB_CACHE"] = model_path


MODEL_NAME = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, cache_dir=model_path)
print(f"✅ Model downloaded and saved in {model_path}")
