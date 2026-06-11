from app.llm.ollama_client import call_ollama
from app.llm.prompts import SYSTEM_PROMPT


def generate_answer(
    question: str,
    contexts: list[str],
    analysis: dict
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
    intent = analysis.get(
        "intent",
        "general"
    )

    if intent == "diagnosis":

        answer_style = """
Start with a clear definition.
Then explain important characteristics.
Then mention incidence or risk factors if available.
"""

    elif intent == "treatment":

        answer_style = """
    Focus on treatment options.
    Mention therapies and management strategies.
    """

    elif intent == "prognosis":

        answer_style = """
    Focus on survival, outcomes, recurrence,
    and prognosis-related information.
    """

    else:

        answer_style = """
    Answer directly using the provided evidence.
    """

    prompt = f"""
You are a medical oncology assistant.

RULES:

Use ONLY information explicitly present in CONTEXT.

Do NOT infer missing facts.

Do NOT add risk factors,
genes,
treatments,
survival statistics,
or pathology details
unless directly mentioned.

If a fact is not explicitly stated,
write:

"Not mentioned in provided sources."

ANSWER STYLE:
{answer_style}

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