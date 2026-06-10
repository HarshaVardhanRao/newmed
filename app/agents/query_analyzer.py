import re


INTENT_PATTERNS = {

    "diagnosis": [
        "diagnosis",
        "diagnose",
        "detect",
        "detection",
        "screening",
        "screen",
        "identify",
        "identified",
        "symptoms",
        "signs"
    ],

    "treatment": [
        "treatment",
        "treat",
        "therapy",
        "therapies",
        "management",
        "manage",
        "surgery",
        "radiotherapy",
        "radiation",
        "chemotherapy",
        "immunotherapy",
        "targeted therapy"
    ],

    "drug": [
        "drug",
        "dose",
        "dosing",
        "medication",
        "medicine",
        "cisplatin",
        "carboplatin",
        "paclitaxel",
        "trastuzumab",
        "tamoxifen"
    ],

    "prognosis": [
        "prognosis",
        "survival",
        "outcome",
        "mortality",
        "life expectancy",
        "recurrence",
        "relapse"
    ],

    "prevention": [
        "prevent",
        "prevention",
        "risk reduction",
        "risk factor",
        "vaccination",
        "vaccine"
    ],

    "staging": [
        "stage",
        "staging",
        "tnm",
        "grade",
        "grading"
    ],

    "side_effects": [
        "side effect",
        "toxicity",
        "adverse effect",
        "complication",
        "complications"
    ]
}


def extract_entities(question):

    entities = []

    cancers = [

        "breast cancer",
        "lung cancer",
        "cervical cancer",
        "prostate cancer",
        "colorectal cancer",
        "ovarian cancer",
        "lymphoma",
        "leukemia",
        "aml",
        "all",
        "melanoma"
    ]

    for cancer in cancers:

        if cancer.lower() in question.lower():

            entities.append(
                cancer
            )

    return entities


def classify_intent(question):

    q = question.lower()

    # -------------------
    # Support Intent
    # -------------------

    SUPPORT_PATTERNS = [
        "i am scared",
        "i am worried",
        "i am afraid",
        "i have cancer",
        "diagnosed with",
        "terrified",
        "anxious"
    ]

    for pattern in SUPPORT_PATTERNS:
        if pattern in q:
            return "support"

    # -------------------
    # Side Effects Intent
    # -------------------

    if any(
        x in q
        for x in [
            "side effect",
            "side effects",
            "toxicity",
            "adverse effect",
            "complication",
            "complications"
        ]
    ):
        return "side_effects"

    # -------------------
    # Prognosis Intent
    # -------------------

    if any(
        x in q
        for x in [
            "prognosis",
            "survival",
            "outcome",
            "mortality",
            "life expectancy",
            "recurrence",
            "relapse"
        ]
    ):
        return "prognosis"

    # -------------------
    # Treatment Intent
    # -------------------

    if any(
        x in q
        for x in [
            "treatment",
            "therapy",
            "management",
            "chemotherapy",
            "radiotherapy",
            "immunotherapy"
        ]
    ):
        return "treatment"

    # -------------------
    # Initialize Scores
    # -------------------

    scores = {
        intent: 0
        for intent in INTENT_PATTERNS
    }

    # -------------------
    # Definition Boost
    # -------------------

    DEFINITION_PATTERNS = [
        "what is",
        "define",
        "definition",
        "meaning of",
        "explain"
    ]

    for pattern in DEFINITION_PATTERNS:

        if pattern in q:
            scores["diagnosis"] += 2

    # -------------------
    # Keyword Scoring
    # -------------------

    for intent, keywords in INTENT_PATTERNS.items():

        for keyword in keywords:

            if keyword in q:
                scores[intent] += 1

    best_intent = max(
        scores,
        key=scores.get
    )

    if scores[best_intent] == 0:
        return "general"

    return best_intent

def estimate_complexity(question):

    words = len(
        question.split()
    )

    if words < 6:
        return "simple"

    if words < 15:
        return "moderate"

    return "complex"


def detect_emotion(question):

    q = question.lower()

    anxiety_words = [

        "scared",
        "worried",
        "afraid",
        "panic",
        "anxious",
        "fear",
        "terrified"
    ]

    for word in anxiety_words:

        if word in q:

            return "anxious"

    return "neutral"


def analyze_query(question):

    return {

        "intent":
            classify_intent(
                question
            ),

        "entities":
            extract_entities(
                question
            ),

        "complexity":
            estimate_complexity(
                question
            ),

        "emotion":
            detect_emotion(
                question
            )
    }