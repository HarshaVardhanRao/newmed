from pprint import pprint

from app.rl.reward_model import (
    reward_model
)


print("\nIntent Rewards\n")

pprint(
    reward_model.get_intent_rewards()
)

print("\nBest Intents\n")

pprint(
    reward_model.get_best_intents()
)

print("\nDiagnosis Strategy\n")

pprint(
    reward_model.suggest_retrieval_depth(
        "diagnosis"
    )
)