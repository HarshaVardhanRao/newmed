from app.retrieval.hybrid_search import (
    HybridRetriever
)

from app.llm.generator import (
    generate_answer
)


retriever = HybridRetriever()


def ask(question: str):

    results = retriever.search(
        question,
        top_k=5
    )

    contexts = [
        r["text"]
        for r in results
    ]

    answer = generate_answer(
        question,
        contexts
    )

    return {
        "answer": answer,
        "sources": results
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