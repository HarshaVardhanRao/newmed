from app.agents.query_analyzer import (
    analyze_query
)

questions = [

    "What is AML?",

    "How is breast cancer treated?",

    "What are side effects of Cisplatin?",

    "What is prognosis of stage 4 lung cancer?",

    "How can cervical cancer be prevented?",

    "I am scared after being diagnosed with lymphoma"
]

for q in questions:

    print("\n")
    print(q)

    print(
        analyze_query(q)
    )