from app.retrieval.hybrid_search import (
    HybridRetriever
)

retriever = HybridRetriever()

query = input("Question: ")

results = retriever.search(
    query=query,
    top_k=5
)

for idx, result in enumerate(
    results,
    start=1
):

    print("\n" + "=" * 80)

    print(
        f"Result {idx}"
    )

    print(
        f"Book: {result['book']}"
    )

    print(
        f"Page: {result['page']}"
    )

    print("-" * 80)

    print(
        result["text"][:1000]
    )