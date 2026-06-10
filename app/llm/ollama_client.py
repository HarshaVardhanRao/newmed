import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen3:8b"  # change if needed


def generate(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]