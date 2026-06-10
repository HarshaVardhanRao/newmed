import requests
import re
import time

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_ollama(prompt):

    start = time.time()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 512
            }
        }
    )

    print(
        "Ollama API:",
        round(time.time() - start, 2),
        "sec"
    )

    data = response.json()

    print("RAW RESPONSE:")
    print(data)

    answer = data.get("response", "")

    answer = re.sub(
        r"<think>.*?</think>",
        "",
        answer,
        flags=re.DOTALL
    )

    return answer.strip()