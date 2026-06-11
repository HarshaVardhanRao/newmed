from app.evaluation.scope_evaluator import (
    scope_evaluator
)

result = scope_evaluator.evaluate(
    question="What is breast cancer?",
    answer="Breast cancer is...",
    contexts=[
        "Breast cancer is the most common..."
    ]
)

print(result)