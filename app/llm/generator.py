from app.llm.ollama_client import call_ollama
from app.llm.prompts import SYSTEM_PROMPT


def generate_answer(
    question: str,
    contexts: list[str]
):

    context_text = ""

    MAX_CHARS = 2500
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

1. Use ONLY the provided context.
2. Summarize relevant information found in the context.
3. If the answer is partially available, provide the partial answer.
4. Combine information from multiple sources when needed.
5. Only say "Information not found in provided sources"
   if absolutely no relevant information exists.

QUESTION:
{question}

CONTEXT:
{context_text}

ANSWER:
"""
    print("\n")
    print("=" * 80)
    print("CONTEXT SENT TO LLM")
    print("=" * 80)
    print(context_text[:5000])
    print("=" * 80)

    return call_ollama(prompt)