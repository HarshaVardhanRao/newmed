import json
from pathlib import Path

FEEDBACK_FILE = Path("data/feedback.json")


def save_feedback(
    question: str,
    answer: str,
    rating: int
):

    # Create file if missing
    if not FEEDBACK_FILE.exists():

        FEEDBACK_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            FEEDBACK_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump([], f)

    # Load existing feedback
    with open(
        FEEDBACK_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        feedback_data = json.load(f)

    # Append new feedback
    feedback_data.append(
        {
            "question": question,
            "answer": answer,
            "rating": rating
        }
    )

    # Save back
    with open(
        FEEDBACK_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            feedback_data,
            f,
            indent=4,
            ensure_ascii=False
        )