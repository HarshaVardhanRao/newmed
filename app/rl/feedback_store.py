import json
from pathlib import Path
from datetime import datetime


FEEDBACK_FILE = (
    "data/rl/feedback.json"
)


class FeedbackStore:

    def __init__(self):

        Path(
            "data/rl"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        if not Path(
            FEEDBACK_FILE
        ).exists():

            with open(
                FEEDBACK_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=2
                )

    def load(self):

        with open(
            FEEDBACK_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def save(
        self,
        question,
        analysis,
        confidence,
        answer,
        feedback
    ):

        data = self.load()

        data.append(

            {
                "timestamp":
                    datetime.now().isoformat(),

                "question":
                    question,

                "analysis":
                    analysis,

                "confidence":
                    confidence,

                "answer":
                    answer,

                "feedback":
                    feedback
            }

        )

        with open(
            FEEDBACK_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

    def stats(self):

        data = self.load()

        if not data:

            return {
                "total": 0,
                "positive": 0,
                "negative": 0,
                "avg_confidence": 0
            }

        positive = sum(
            1
            for item in data
            if item["feedback"] == 1
        )

        negative = sum(
            1
            for item in data
            if item["feedback"] == 0
        )

        avg_confidence = sum(
            item["confidence"]
            for item in data
        ) / len(data)

        return {

            "total":
                len(data),

            "positive":
                positive,

            "negative":
                negative,

            "avg_confidence":
                round(
                    avg_confidence,
                    3
                )
        }


feedback_store = (
    FeedbackStore()
)