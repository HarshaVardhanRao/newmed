from app.retrieval.hybrid_search import (
    HybridRetriever
)

from app.llm.generator import (
    generate_answer
)

import time

retriever = HybridRetriever()


def ask(question: str):

    start = time.time()
    results = retriever.search(question, top_k=3)
    print("Retrieval:", round(time.time() - start, 2), "sec")

    contexts = [
        r["text"]
        for r in results
    ]

    start = time.time()
    answer = generate_answer(
        question,
        contexts
    )
    print("Generation:", round(time.time() - start, 2), "sec")

    return {
    "answer": answer,
    "sources": results,
    "retrieved_docs": contexts,
    "retrieval_count": len(results)
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
