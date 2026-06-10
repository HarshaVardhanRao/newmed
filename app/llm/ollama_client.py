import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen3:8b"  # change if needed

import time

def generate(prompt: str):

    start = time.time()
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
            "num_predict": 120,
            "temperature": 0.1
            }
        },
        timeout=300
    )
    print(
    "Ollama API:",
    round(time.time()-start,2),
    "sec"
    )
    response.raise_for_status()

    return response.json()["response"]