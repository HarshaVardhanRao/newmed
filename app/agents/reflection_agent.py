from app.llm.ollama_client import (
    call_ollama
)


class ReflectionAgent:

    def reflect(
        self,
        question,
        answer,
        contexts
    ):

        context_text = "\n\n".join(
            contexts[:4]
        )

        prompt = f"""
You are a medical answer verifier.

QUESTION:
{question}

CONTEXT:
{context_text}

ANSWER:
{answer}

TASK:

1. Remove statements not supported by CONTEXT.
2. Remove hallucinations.
3. Keep only evidence-supported claims.
4. Improve clarity.

Return revised answer only.
"""

        return call_ollama(
            prompt
        )


reflector = ReflectionAgent()