from typing import Dict


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

    return plan