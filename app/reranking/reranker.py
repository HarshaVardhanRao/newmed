from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, chunks, top_k=5):

    pairs = [
        (query, chunk["text"])
        for chunk in chunks
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(scores, chunks),
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        chunk
        for score, chunk in ranked[:top_k]
    ]