from app.llm.ollama_client import generate
from app.llm.prompts import SYSTEM_PROMPT


def generate_answer(
    question: str,
    contexts: list[str]
):

    context_text = ""

    for idx, chunk in enumerate(contexts, start=1):

        context_text += (
            f"\n\nSOURCE {idx}\n"
            f"{chunk}"
        )

    prompt = f"""
{SYSTEM_PROMPT}

QUESTION:
{question}

CONTEXT:
{context_text}

ANSWER:
"""

    return generate(prompt)