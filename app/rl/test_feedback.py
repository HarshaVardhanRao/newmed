from app.rl.feedback_store import (
    feedback_store
)

feedback_store.save(
    question="What is breast cancer?",
    analysis={
        "intent":"diagnosis"
    },
    confidence=0.85,
    answer="...",
    feedback=1
)

feedback_store.save(
    question="What is AML?",
    analysis={
        "intent":"diagnosis"
    },
    confidence=0.75,
    answer="...",
    feedback=1
)

feedback_store.save(
    question="Stage 4 lung cancer prognosis",
    analysis={
        "intent":"prognosis"
    },
    confidence=0.82,
    answer="...",
    feedback=1
)

feedback_store.save(
    question="Rare ALK mutation",
    analysis={
        "intent":"diagnosis"
    },
    confidence=0.52,
    answer="...",
    feedback=0
)

print("Saved")