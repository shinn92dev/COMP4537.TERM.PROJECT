import os
from fastapi import APIRouter
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


router = APIRouter()

# Load Google FLAN-T5 Model
model_path = os.path.abspath("../ai_models")
os.environ["HUGGINGFACE_HUB_CACHE"] = model_path


MODEL_NAME = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, cache_dir=model_path)
print(f"✅ Model downloaded and saved in {model_path}")


def ask_to_ai(prompt=None):
    # Define the input prompt
    if not prompt:
        prompt = "Hello. Let me know one fun fact that I might not know."
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    outputs = model.generate(
        input_ids,
        do_sample=True,
        max_length=100,
        temperature=0.7,
        top_p=0.9,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id
    )

    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(decoded_output)


ask_to_ai()
