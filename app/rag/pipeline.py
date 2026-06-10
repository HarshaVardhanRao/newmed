from app.retrieval.hybrid_search import (
    HybridRetriever
)

from app.llm.generator import (
    generate_answer
)

import time
from app.agents.response_optimizer import (
    optimizer
)


retriever = HybridRetriever()


def ask(question: str):

    start = time.time()

    search_results = retriever.search(
        question,
        top_k=8
    )
    analysis = search_results["analysis"]
    retrieved_results = search_results["results"]

    optimized_results = optimizer.optimize(
    retrieved_results,
    question
)

    print(
        "Retrieval:",
        round(time.time() - start, 2),
        "sec"
    )


    print(
        "Query Analysis:",
        analysis
    )

    print(
        "Retrieved:",
        len(retrieved_results)
    )

    print(
        "After Optimization:",
        len(optimized_results)
    )

    contexts = [
        r["text"]
        for r in optimized_results
    ]

    start = time.time()

    answer = generate_answer(
        question,
        contexts
    )

    print(
        "Generation:",
        round(time.time() - start, 2),
        "sec"
    )
    print("\nRETRIEVED CONTEXTS\n")

    for i, c in enumerate(contexts, start=1):

        print("\n" + "=" * 80)

        print(f"CHUNK {i}")

        print(c[:1000])

    return {

        "answer": answer,

        "analysis": analysis,

        "sources": optimized_results,

        "retrieved_docs": contexts,

        "retrieval_count": len(optimized_results)
    }


if __name__ == "__main__":

    while True:

        question = input(
            "\nQuestion: "
        )

        if question.lower() == "exit":
            break

        result = ask(question)

        print(
            "\nQUERY ANALYSIS:\n"
        )

        print(
            result["analysis"]
        )

        print(
            "\nANSWER:\n"
        )

        print(
            result["answer"]
        )

        print(
            "\nSOURCES:\n"
        )

        for idx, source in enumerate(
            result["sources"],
            start=1
        ):

            print(
                f"{idx}. "
                f"{source['book']} "
                f"(Page {source['page']})"
            )

    