import json
from statistics import mean

from app.evaluation.scope_evaluator import (
    scope_evaluator
)

from app.rl.reward_model import (
    reward_model
)


class DeepEvaluator:

    def __init__(self):

        self.scope_scores = []

        self.confidences = []


    def evaluate_answer(

        self,

        question,
        answer,
        contexts,
        confidence

    ):

        scope = (
            scope_evaluator.evaluate(
                question,
                answer,
                contexts
            )
        )

        self.scope_scores.append(
            scope
        )

        self.confidences.append(
            confidence
        )

        return scope
    
    def summary(self):

        if not self.scope_scores:

            return {}

        metrics = {}

        keys = [

            "Safety",
            "Completeness",
            "Originality",
            "Precision",
            "Evidence"

        ]

        for key in keys:

            values = [

                score.get(
                    key,
                    0
                )

                for score in self.scope_scores

            ]

            metrics[key] = round(
                mean(values),
                3
            )

        metrics[
            "Confidence"
        ] = round(
            mean(
                self.confidences
            ),
            3
        )

        rl_stats = (
            reward_model
            .get_intent_rewards()
        )

        metrics[
            "RL_Intent_Rewards"
        ] = rl_stats

        return metrics

    def save_report(
        self,
        path
    ):

        report = self.summary()

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )

        return report


deep_evaluator = (
    DeepEvaluator()
)