from app.llm.ollama_client import call_ollama


def generate_answer(
    question: str,
    contexts: list[str],
    analysis: dict
):

    context_text = ""

    MAX_CHARS = 2000

    for idx, chunk in enumerate(
        contexts[:4],
        start=1
    ):

        context_text += (
            f"\n\nSOURCE {idx}\n"
            f"{chunk[:MAX_CHARS]}"
        )

    print(
        f"Context count: {min(len(contexts),4)}"
    )

    print(
        f"Context chars: {len(context_text)}"
    )

    intent = analysis.get(
        "intent",
        "general"
    )

    # -------------------
    # Answer Planner
    # -------------------

    PLANS = {

        "diagnosis": """
1. Definition
2. Key Characteristics
3. Risk Factors (only if present)
""",

        "treatment": """
1. Standard Treatment
2. Treatment Options
3. Important Notes
""",

        "prognosis": """
1. Prognosis
2. Factors Affecting Outcome
3. Survival or Recurrence Information
""",

        "side_effects": """
1. Common Side Effects
2. Serious Side Effects
3. Monitoring Considerations
""",

        "prevention": """
1. Prevention Methods
2. Screening
3. Risk Reduction
""",

        "support": """
1. Acknowledge Concern
2. Provide Relevant Information
3. Encourage Medical Follow-up
"""
    }

    answer_plan = PLANS.get(
        intent,
        """
1. Direct Answer
2. Supporting Information
"""
    )

    prompt = f"""
You are a medical oncology assistant.

RULES:

1. Use ONLY information explicitly present in CONTEXT.

2. Do NOT use outside knowledge.

3. Do NOT invent:
   - risk factors
   - genes
   - treatments
   - survival statistics
   - pathology findings

4. If information is missing, write:

   "Not mentioned in provided sources."

5. Follow the ANSWER PLAN.

6. Prefer concise evidence-grounded answers.

QUESTION:
{question}

INTENT:
{intent}

ANSWER PLAN:
{answer_plan}

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