from app.llm.ollama_client import (
    call_ollama
)


class SelfCritiqueAgent:

    def critique(
        self,
        question,
        answer,
        confidence
    ):

        if confidence >= 0.7:
            return answer

        prompt = f"""
You are a medical QA reviewer.

QUESTION:
{question}

ANSWER:
{answer}

The confidence score is {confidence}.

Check:

1. Missing information
2. Unsupported claims
3. Ambiguous statements

Return an improved answer.
"""

        return call_ollama(
            prompt
        )


self_critique_agent = (
    SelfCritiqueAgent()
)