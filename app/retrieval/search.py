from app.retrieval.embeddings import embed_texts
from app.retrieval.vector_store import collection


def search(query: str, top_k: int = 5):

    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    query = input("Question: ")

    results = search(query)

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for i, (doc, meta) in enumerate(zip(docs, metas), start=1):

        print("\n" + "=" * 80)
        print(f"Result {i}")
        print(f"Book: {meta['book']}")
        print(f"Page: {meta['page']}")
        print("-" * 80)

        print(doc[:1000])