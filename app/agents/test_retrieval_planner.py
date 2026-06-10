from app.agents.retrieval_planner import (
    plan_retrieval
)

examples = [

    {
        "intent": "diagnosis",
        "complexity": "simple",
        "emotion": "neutral"
    },

    {
        "intent": "treatment",
        "complexity": "moderate",
        "emotion": "neutral"
    },

    {
        "intent": "prognosis",
        "complexity": "complex",
        "emotion": "neutral"
    },

    {
        "intent": "support",
        "complexity": "moderate",
        "emotion": "anxious"
    }
]

for e in examples:

    print(
        "\nAnalysis:"
    )

    print(e)

    print(
        "\nPlan:"
    )

    print(
        plan_retrieval(e)
    )