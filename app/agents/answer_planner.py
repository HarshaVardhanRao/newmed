class AnswerPlanner:

    def plan(
        self,
        analysis
    ):

        intent = analysis["intent"]

        templates = {

            "diagnosis": [
                "Definition",
                "Key Characteristics",
                "Risk Factors"
            ],

            "treatment": [
                "Standard Treatment",
                "Treatment Options",
                "Important Notes"
            ],

            "prognosis": [
                "Prognosis",
                "Factors Affecting Outcome"
            ],

            "side_effects": [
                "Common Side Effects",
                "Serious Side Effects"
            ],

            "prevention": [
                "Prevention Methods",
                "Screening"
            ]
        }

        return templates.get(
            intent,
            ["Answer"]
        )


answer_planner = AnswerPlanner()