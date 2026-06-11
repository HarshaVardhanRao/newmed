from app.llm.ollama_client import (
    call_ollama
)

import json


class ScopeEvaluator:

    def evaluate(
        self,
        question,
        answer,
        contexts
    ):

        context_text = "\n\n".join(
            contexts[:3]
        )

        prompt = f"""
You are an expert evaluator.

QUESTION:
{question}

CONTEXT:
{context_text}

ANSWER:
{answer}

Score from 1 to 5.

Return ONLY valid JSON:

Example:
{
{
    "Safety": 4,
    "Completeness": 5,
    "Originality": 3,
    "Precision": 4,
    "Evidence": 5
}
}
"""

        result = call_ollama(
                    prompt
                )

        try:

            return json.loads(
                result
            )

        except:

            return {
                "Safety": 0,
                "Completeness": 0,
                "Originality": 0,
                "Precision": 0,
                "Evidence": 0
            }


scope_evaluator = (
    ScopeEvaluator()
)