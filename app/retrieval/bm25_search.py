import json
from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(
        self,
        chunks_path: str = "data/processed/chunks.json"
    ):

        with open(
            chunks_path,
            "r",
            encoding="utf-8"
        ) as f:
            self.chunks = json.load(f)

        self.corpus = [
            chunk["text"].lower().split()
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(self.corpus)

    def search(
        self,
        query: str,
        top_k: int = 10
    ):
        import re

        tokens = re.findall(
            r"\w+",
            query.lower()
        )

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(scores, self.chunks),
            reverse=True,
            key=lambda x: x[0]
        )

        return [
            {
                "score": float(score),
                "chunk": chunk
            }
            for score, chunk in ranked[:top_k]
        ]