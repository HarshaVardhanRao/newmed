class PatientAgent:

    def rewrite(
        self,
        answer,
        analysis
    ):

        if analysis["emotion"] == "anxious":

            return (
                answer +
                "\n\nIf you are concerned about symptoms or diagnosis, consult your healthcare provider for personalized guidance."
            )

        return answer


patient_agent = PatientAgent()