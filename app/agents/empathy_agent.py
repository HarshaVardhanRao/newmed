class EmpathyAgent:

    def apply(
        self,
        answer,
        analysis
    ):

        emotion = analysis.get(
            "emotion",
            "neutral"
        )

        if emotion == "anxious":

            prefix = (
                "I understand this can be a stressful situation.\n\n"
            )

            return prefix + answer

        return answer


empathy_agent = EmpathyAgent()