class ConfidenceAgent:

    def score(
        self,
        chunks,
        answer,
        analysis
    ):

        if not chunks:
            return 0.0

        score = 0.0

        # -------------------
        # Evidence Coverage
        # -------------------

        evidence_score = min(
            len(chunks) / 4,
            1.0
        )

        score += evidence_score * 0.4

        # -------------------
        # Context Volume
        # -------------------

        context_chars = len(
            " ".join(
                chunk["text"]
                for chunk in chunks
            )
        )

        context_score = min(
            context_chars / 4000,
            1.0
        )

        score += context_score * 0.3

        # -------------------
        # Entity Coverage
        # -------------------

        entities = analysis.get(
            "entities",
            []
        )

        if entities:

            matched = 0

            combined_text = (
                answer.lower()
                + " "
                + " ".join(
                    c["text"].lower()
                    for c in chunks
                )
            )

            for entity in entities:

                if entity.lower() in combined_text:
                    matched += 1

            entity_score = (
                matched /
                len(entities)
            )

            score += entity_score * 0.2

        else:

            score += 0.2

        # -------------------
        # Minimum Grounding Bonus
        # -------------------

        score += 0.1

        return round(
            min(score, 1.0),
            3
        )


confidence_agent = (
    ConfidenceAgent()
)