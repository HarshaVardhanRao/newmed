from app.llm.ollama_client import call_ollama
from app.llm.prompts import SYSTEM_PROMPT


def generate_answer(
    question: str,
    contexts: list[str]
):

    context_text = ""

    MAX_CHARS = 800

    for idx, chunk in enumerate(
        contexts[:4],
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
You are a medical oncology assistant.

RULES:

1. Use ONLY information present in CONTEXT.
2. Do NOT use outside knowledge.
3. If answer is not found, say:
   "Information not found in provided sources."
4. Be concise.
5. Quote specific facts from context.

QUESTION:
{question}

CONTEXT:
{context_text}

ANSWER:
"""
    return call_ollama(prompt)