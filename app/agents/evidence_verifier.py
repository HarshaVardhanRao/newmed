INTENT_REJECTS = {
    "diagnosis": [
        "pregnancy",
        "chemotherapy",
        "radiotherapy",
        "management",
        "treatment",
        "stage iv"
    ],

    "treatment": [
        "epidemiology",
        "incidence"
    ],

    "prognosis": [
        "screening",
        "prevention"
    ]
}


class EvidenceVerifier:

    def verify(self, chunks, analysis):

        intent = analysis["intent"]

        reject_terms = INTENT_REJECTS.get(
            intent,
            []
        )

        filtered = []

        for chunk in chunks:

            text = chunk["text"].lower()

            reject = any(
                term in text
                for term in reject_terms
            )

            if not reject:
                filtered.append(chunk)

        return filtered
    
verifier = EvidenceVerifier()