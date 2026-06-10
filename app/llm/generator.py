from app.llm.ollama_client import call_ollama
from app.llm.prompts import SYSTEM_PROMPT


def generate_answer(
    question: str,
    contexts: list[str]
):

    context_text = ""

    MAX_CHARS = 1500

    for idx, chunk in enumerate(
        contexts[:5],
        start=1
    ):

        context_text += (
            f"\n\nSOURCE {idx}\n"
            f"{chunk[:MAX_CHARS]}"
        )

    print(
        f"Context count: {min(len(contexts),3)}"
    )

    print(
        f"Context chars: {len(context_text)}"
    )

    prompt = f"""
{SYSTEM_PROMPT}

QUESTION:
{question}

CONTEXT:
{context_text}

ANSWER:
"""

    return call_ollama(prompt)