from app.retrieval.hybrid_search import (
    HybridRetriever
)
from app.agents.confidence_agent import (
    confidence_agent
)

from app.agents.evidence_verifier import (
    verifier
)

from app.agents.reflection_agent import (
    reflector
)

from app.agents.self_critique_agent import (
    self_critique_agent
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
        question,
        analysis
        )
    
    verified_results = verifier.verify(
        optimized_results,
        analysis
    )
    if analysis["complexity"] == "simple":

        verified_results = verified_results[:2]

    elif analysis["complexity"] == "moderate":

        verified_results = verified_results[:4]

    else:

        verified_results = verified_results[:6]
    if not verified_results:
        verified_results = optimized_results[:2]

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

    print(
        "After Verification:",
        len(verified_results)
    )
    confidence = confidence_agent.score(
        analysis,
        retrieved_results,
        verified_results
    )
    
    print(
        "Confidence:",
        confidence
    )
    contexts = [
        r["text"]
        for r in verified_results
    ]

    start = time.time()

    # Generate first
    answer = generate_answer(
        question,
        contexts,
        analysis
    )

    # Then reflect
    answer = reflector.reflect(
        question,
        answer,
        contexts
    )
    answer = self_critique_agent.critique(
        question,
        answer,
        confidence
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
    "confidence": round(confidence, 2),
    "sources": verified_results,
    "retrieved_docs": contexts
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

    