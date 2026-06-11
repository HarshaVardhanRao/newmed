import re

SECTION_BOOSTS = {

    "diagnosis": [
        "definition",
        "overview",
        "introduction",
        "epidemiology",
        "etiology",
        "pathology"
    ],

    "treatment": [
        "treatment",
        "management",
        "therapy",
        "chemotherapy",
        "radiotherapy",
        "immunotherapy"
    ],

    "prognosis": [
        "prognosis",
        "survival",
        "outcome",
        "mortality",
        "recurrence"
    ],

    "prevention": [
        "prevention",
        "screening",
        "risk reduction"
    ],

    "side_effects": [
        "toxicity",
        "side effects",
        "adverse effects",
        "complications"
    ]
}
class ResponseOptimizer:

    def __init__(
        self,
        max_chunks=4,
        max_chunk_chars=1200
    ):
        self.max_chunks = max_chunks
        self.max_chunk_chars = max_chunk_chars

    def remove_duplicates(
        self,
        chunks
    ):

        seen = set()
        unique = []

        for chunk in chunks:

            text = chunk["text"]

            key = text[:300].lower()

            if key in seen:
                continue

            seen.add(key)

            unique.append(chunk)

        return unique

    def remove_short_chunks(
        self,
        chunks
    ):

        filtered = []

        for chunk in chunks:

            if len(
                chunk["text"].split()
            ) < 40:
                continue

            filtered.append(chunk)

        return filtered

    def score_chunk(
    self,
    chunk,
    question,
    analysis
):

        text = chunk["text"].lower()

        score = 0

        # -------------------
        # Keyword overlap
        # -------------------

        for word in question.lower().split():

            if word in text:
                score += 1

        # -------------------
        # Entity boost
        # -------------------

        for entity in analysis.get(
            "entities",
            []
        ):

            if entity.lower() in text:
                score += 10

        # -------------------
        # Intent boost
        # -------------------

        intent = analysis.get(
            "intent",
            "general"
        )

        boosts = SECTION_BOOSTS.get(
            intent,
            []
        )

        for keyword in boosts:

            if keyword in text:
                score += 5

        return score

    def rank_chunks(
        self,
        chunks,
        query
    ):

        ranked = sorted(
            chunks,
            key=lambda x: self.score_chunk(
                x,
                query
            ),
            reverse=True
        )

        return ranked

    def trim_chunk(
        self,
        text
    ):

        return text[
            :self.max_chunk_chars
        ]

    def optimize(
        self,
        chunks,
        query
    ):

        chunks = self.remove_duplicates(
            chunks
        )

        chunks = self.remove_short_chunks(
            chunks
        )

        chunks = self.rank_chunks(
            chunks,
            query
        )

        chunks = chunks[
            :self.max_chunks
        ]

        optimized = []

        for chunk in chunks:

            optimized.append(
                {
                    **chunk,
                    "text": self.trim_chunk(
                        chunk["text"]
                    )
                }
            )

        return optimized


optimizer = ResponseOptimizer()