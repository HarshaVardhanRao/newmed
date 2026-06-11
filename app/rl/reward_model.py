from collections import defaultdict

from app.rl.feedback_store import (
    feedback_store
)


class RewardModel:

    def __init__(self):

        self.feedback = (
            feedback_store
        )

    def calculate_rewards(self):

        data = self.feedback.load()

        rewards = defaultdict(
            lambda: {
                "count": 0,
                "reward": 0
            }
        )

        for item in data:

            intent = item[
                "analysis"
            ].get(
                "intent",
                "general"
            )

            confidence = item[
                "confidence"
            ]

            feedback = item[
                "feedback"
            ]

            reward = (
                confidence
                if feedback == 1
                else -confidence
            )

            rewards[intent][
                "count"
            ] += 1

            rewards[intent][
                "reward"
            ] += reward

        return rewards

    def get_intent_rewards(self):

        rewards = (
            self.calculate_rewards()
        )

        output = {}

        for intent, data in rewards.items():

            avg_reward = (
                data["reward"]
                / data["count"]
            )

            output[intent] = {

                "samples":
                    data["count"],

                "avg_reward":
                    round(
                        avg_reward,
                        3
                    )
            }

        return output

    def get_best_intents(self):

        rewards = (
            self.get_intent_rewards()
        )

        ranked = sorted(

            rewards.items(),

            key=lambda x:
                x[1][
                    "avg_reward"
                ],

            reverse=True
        )

        return ranked

    def suggest_retrieval_depth(
        self,
        intent
    ):

        rewards = (
            self.get_intent_rewards()
        )

        score = rewards.get(
            intent,
            {}
        ).get(
            "avg_reward",
            0
        )

        if score > 0.8:

            return {
                "top_k": 4,
                "rerank_k": 8
            }

        elif score > 0.5:

            return {
                "top_k": 6,
                "rerank_k": 12
            }

        else:

            return {
                "top_k": 8,
                "rerank_k": 16
            }


reward_model = (
    RewardModel()
)