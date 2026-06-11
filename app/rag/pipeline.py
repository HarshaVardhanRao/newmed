from app.retrieval.hybrid_search import (
    HybridRetriever
)
from app.agents.confidence_agent import (
    confidence_agent
)
from app.agents.empathy_agent import (
    empathy_agent
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
from app.evaluation.scope_evaluator import (
    scope_evaluator
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

    contexts = [
        r["text"]
        for r in verified_results
    ]

    # Generate first

    generation_start = time.time()
    
    answer = generate_answer(
        question,
        contexts,
        analysis
    )
    print("Generation:", round(time.time()-generation_start,2))

    answer = empathy_agent.apply(
        answer,
        analysis
    )
    confidence = confidence_agent.score(
        verified_results,
        answer,
        analysis
    )
    
    print(
        "Confidence:",
        confidence
    )
    # Then reflect

    reflection_start = time.time()
    answer = reflector.reflect(
        question,
        answer,
        contexts
    )
    print("Reflection:", round(time.time()-reflection_start,2))

    self_critique_agent_start = time.time()
    answer = self_critique_agent.critique(
        question,
        answer,
        confidence
    )
    print("Self Critique:", round(time.time()-self_critique_agent_start,2))

    scope_start = time.time()
    scope_scores = (
        scope_evaluator.evaluate(
            question,
            answer,
            contexts
        )
    )
    print("Reflection:", round(time.time()-scope_start,2))

    
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
    "scope": scope_scores,
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

    