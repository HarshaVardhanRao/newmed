from typing import Dict
from app.rl.reward_model import (
    reward_model
)

def plan_retrieval(
    analysis: Dict
):

    intent = analysis[
        "intent"    
    ]

    complexity = analysis[
        "complexity"
    ]

    emotion = analysis[
        "emotion"
    ]

    plan = {

        "bm25_k": 25,

        "semantic_k": 25,

        "candidate_pool": 30,

        "rerank_top_k": 8,

        "bm25_weight": 0.4,

        "semantic_weight": 0.6
    }
    strategy = (
        reward_model
        .suggest_retrieval_depth(
            analysis["intent"]
        )
    )

    print(
        "RL Strategy:",
        strategy
    )

    # ------------------
    # Intent Planning
    # ------------------

    if intent == "diagnosis":

        plan.update({

            "bm25_k": 20,

            "semantic_k": 25,

            "candidate_pool": 30
        })

    elif intent == "treatment":

        plan.update({

            "bm25_k": 30,

            "semantic_k": 30,

            "candidate_pool": 40
        })

    elif intent == "prognosis":

        plan.update({

            "bm25_k": 30,

            "semantic_k": 35,

            "candidate_pool": 45
        })

    elif intent == "side_effects":

        plan.update({

            "bm25_k": 35,

            "semantic_k": 25,

            "candidate_pool": 40
        })

    elif intent == "prevention":

        plan.update({

            "bm25_k": 25,

            "semantic_k": 30,

            "candidate_pool": 35
        })

    elif intent == "support":

        plan.update({

            "bm25_k": 15,

            "semantic_k": 25,

            "candidate_pool": 25
        })

    # ------------------
    # Complexity Planning
    # ------------------

    if complexity == "moderate":

        plan["candidate_pool"] += 10

    elif complexity == "complex":

        plan["candidate_pool"] += 20

    # ------------------
    # Emotion Planning
    # ------------------

    if emotion == "anxious":

        plan["candidate_pool"] += 5

    # ------------------
    # RL Adaptation
    # ------------------

    strategy = (
        reward_model
        .suggest_retrieval_depth(
            analysis["intent"]
        )
    )

    print(
        "RL Strategy:",
        strategy
    )

    plan["candidate_pool"] = max(
        plan["candidate_pool"],
        strategy["top_k"] * 4
    )

    plan["rerank_top_k"] = max(
        plan["rerank_top_k"],
        strategy["rerank_k"]
    )

    return plan
