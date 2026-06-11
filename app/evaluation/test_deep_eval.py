from pprint import pprint

from app.evaluation.deep_eval import (
    deep_evaluator
)

deep_evaluator.evaluate_answer(

    question=
    "What is breast cancer?",

    answer=
    "Breast cancer is...",

    contexts=[
        "Breast cancer..."
    ],

    confidence=0.81
)

deep_evaluator.evaluate_answer(

    question=
    "What is AML?",

    answer=
    "AML is...",

    contexts=[
        "AML..."
    ],

    confidence=0.73
)

pprint(
    deep_evaluator.summary()
)