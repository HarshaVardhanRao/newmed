from app.llm.ollama_client import call_ollama


def call_judge(prompt):

    return call_ollama(
        prompt,
        model="llama3.1:8b"
    )