def expand_query(
    question,
    analysis
):

    intent = analysis[
        "intent"
    ]

    expanded = question

    entities = analysis.get(
        "entities",
        []
    )

    for entity in entities:

        expanded += f" {entity}"

    if (
        intent == "diagnosis"
        and analysis["complexity"] == "simple"
    ):

        expanded += (
            " definition "
            "overview "
            "introduction "
            "epidemiology "
            "etiology"
        )
    
    elif intent == "prognosis":

        expanded += (
            " prognosis "
            "survival "
            "mortality "
            "outcome "
            "life expectancy "
            "advanced stage "
            "metastatic disease"
        )

    elif intent == "treatment":

        expanded += (
            " treatment therapy "
            "management chemotherapy "
            "radiotherapy immunotherapy"
        )

    elif intent == "side_effects":

        expanded += (
            " toxicity adverse effects "
            "complications safety"
        )

    elif intent == "diagnosis":

        expanded += (
            " definition "
            "overview "
            "introduction "
            "epidemiology "
            "etiology "
            "pathology"
        )

    elif intent == "prevention":

        expanded += (
            " prevention screening "
            "risk reduction prophylaxis"
        )

    return expanded