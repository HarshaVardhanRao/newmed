from collections import defaultdict

from app.retrieval.bm25_search import BM25Retriever
from app.retrieval.embeddings import embed_texts
from app.retrieval.vector_store import collection
import time

from app.reranking.reranker import rerank
from app.agents.query_analyzer import (
    analyze_query
)
from app.agents.retrieval_planner import (
    plan_retrieval
)




class HybridRetriever:

    def __init__(self):

        self.bm25 = BM25Retriever()

    def semantic_search(
        self,
        query: str,
        top_k: int = 10
    ):

        embedding = embed_texts([query])[0]

        results = collection.query(
            query_embeddings=[
                embedding.tolist()
            ],
            n_results=top_k
        )

        output = []

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        ids = results["ids"][0]

        for doc, meta, chunk_id in zip(
            docs,
            metas,
            ids
        ):
            output.append(
                {
                    "chunk_id": chunk_id,
                    "text": doc,
                    "book": meta["book"],
                    "page": meta["page"]
                }
            )

        return output

    def search(
        self,
        query: str,
        top_k: int = 8
    ):

        analysis = analyze_query(query)

        print(
            f"Intent: {analysis['intent']}"
        )

        print(
            f"Complexity: {analysis['complexity']}"
        )

        print(
            f"Emotion: {analysis['emotion']}"
        )

        intent = analysis["intent"]

        plan = plan_retrieval(
            analysis
        )

        print(
            "Retrieval Plan:",
            plan
        )

        bm25_k = plan[
            "bm25_k"
        ]

        semantic_k = plan[
            "semantic_k"
        ]

        candidate_pool = plan[
            "candidate_pool"
        ]

        rerank_top_k = plan[
            "rerank_top_k"
        ]

        start = time.time()



        bm25_results = self.bm25.search(
            query,
            top_k=bm25_k
        )
        print("BM25:", round(time.time() - start, 2), "sec")

        start = time.time()
        semantic_results = self.semantic_search(
            query,
            top_k=semantic_k
        )
        print("Semantic:", round(time.time() - start, 2), "sec")



        combined = defaultdict(
            lambda: {
                "score": 0,
                "data": None
            }
        )

        # BM25 score contribution
        for rank, item in enumerate(
            bm25_results,
            start=1
        ):

            chunk = item["chunk"]

            chunk_id = chunk["chunk_id"]

            combined[chunk_id]["score"] += (
                plan["bm25_weight"] / rank
            )

            combined[chunk_id]["data"] = chunk

        # Semantic score contribution
        for rank, item in enumerate(
            semantic_results,
            start=1
        ):

            chunk_id = item["chunk_id"]

            combined[chunk_id]["score"] += (
                plan["semantic_weight"] / rank
            )

            combined[chunk_id]["data"] = {
                "chunk_id": chunk_id,
                "book": item["book"],
                "page": item["page"],
                "text": item["text"]
            }

        final_results = sorted(
            combined.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        

        candidate_pool = 30

        if analysis["complexity"] == "moderate":
            candidate_pool = 40

        elif analysis["complexity"] == "complex":
            candidate_pool = 50

        candidates = [
            item["data"]
            for item in final_results[:candidate_pool]
        ]

        start = time.time()
        reranked = rerank(
            query=query,
            chunks=candidates,
            top_k=rerank_top_k
        )
        print("Rerank:", round(time.time() - start, 2), "sec")

        return {
            "analysis": analysis,
            "results": reranked
        }