class ConfidenceAgent:

    def score(
        self,
        analysis,
        retrieved_results,
        verified_results
    ):

        score = 0.0

        # -------------------
        # Retrieval Coverage
        # -------------------

        score += min(
            len(verified_results) / 5,
            1.0
        ) * 0.4

        # -------------------
        # Entity Coverage
        # -------------------

        entities = analysis.get(
            "entities",
            []
        )

        if entities:

            score += 0.3

        # -------------------
        # Complexity
        # -------------------

        complexity = analysis.get(
            "complexity",
            "simple"
        )

        if complexity == "simple":

            score += 0.3

        elif complexity == "moderate":

            score += 0.2

        else:

            score += 0.1

        return round(
            min(score, 1.0),
            2
        )


confidence_agent = ConfidenceAgent()