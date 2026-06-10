import json
import time

from nltk.translate.bleu_score import (
    sentence_bleu,
    SmoothingFunction
)

from rouge_score import rouge_scorer

from bert_score import score

from sentence_transformers import (
    SentenceTransformer,
    util
)

from app.rag.pipeline import ask
from app.retrieval.hybrid_search import HybridRetriever


retriever = HybridRetriever()

embedder = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

smooth = SmoothingFunction().method1

rouge = rouge_scorer.RougeScorer(
    ["rouge1", "rouge2", "rougeL"],
    use_stemmer=True
)


def bleu_scores(reference, prediction):

    bleu1 = sentence_bleu(
        [reference.split()],
        prediction.split(),
        weights=(1, 0, 0, 0),
        smoothing_function=smooth
    )

    bleu2 = sentence_bleu(
        [reference.split()],
        prediction.split(),
        weights=(0.5, 0.5, 0, 0),
        smoothing_function=smooth
    )

    bleu4 = sentence_bleu(
        [reference.split()],
        prediction.split(),
        smoothing_function=smooth
    )

    return bleu1, bleu2, bleu4


def rouge_scores(reference, prediction):

    scores = rouge.score(
        reference,
        prediction
    )

    return (
        scores["rouge1"].fmeasure,
        scores["rouge2"].fmeasure,
        scores["rougeL"].fmeasure
    )


def bert_score_metric(reference, prediction):

    _, _, f1 = score(
        [prediction],
        [reference],
        lang="en",
        verbose=False
    )

    return f1.mean().item()


def semantic_similarity(text1, text2):

    emb1 = embedder.encode(
        text1,
        convert_to_tensor=True
    )

    emb2 = embedder.encode(
        text2,
        convert_to_tensor=True
    )

    return util.cos_sim(
        emb1,
        emb2
    ).item()


def evaluate():

    with open(
        "data/benchmark/benchmark_qa.json",
        "r",
        encoding="utf-8"
    ) as f:

        benchmark = json.load(f)

    print(
        f"Loaded {len(benchmark)} benchmark questions"
    )

    n = len(benchmark)

    total_bleu1 = 0
    total_bleu2 = 0
    total_bleu4 = 0

    total_rouge1 = 0
    total_rouge2 = 0
    total_rougeL = 0

    total_bert = 0

    total_answer_rel = 0
    total_context_rel = 0
    total_faithfulness = 0

    total_hit = 0
    total_latency = 0

    for idx, item in enumerate(
        benchmark,
        start=1
    ):

        question = item["q"]

        reference = item["a"]

        print(
            f"[{idx}/{n}] "
            f"{item['id']}"
        )

        start = time.time()

        result = ask(question)

        latency = (
            time.time() - start
        )

        total_latency += latency

        prediction = result["answer"]

        contexts = [
            s["text"]
            for s in result["sources"]
        ]

        context_text = " ".join(
            contexts
        )

        if len(result["sources"]) > 0:
            total_hit += 1

        bleu1, bleu2, bleu4 = (
            bleu_scores(
                reference,
                prediction
            )
        )

        total_bleu1 += bleu1
        total_bleu2 += bleu2
        total_bleu4 += bleu4

        r1, r2, rl = rouge_scores(
            reference,
            prediction
        )

        total_rouge1 += r1
        total_rouge2 += r2
        total_rougeL += rl

        bert = bert_score_metric(
            reference,
            prediction
        )

        total_bert += bert

        answer_rel = semantic_similarity(
            prediction,
            reference
        )

        total_answer_rel += answer_rel

        context_rel = semantic_similarity(
            question,
            context_text
        )

        total_context_rel += context_rel

        faithfulness = semantic_similarity(
            prediction,
            context_text
        )

        total_faithfulness += faithfulness

        print(
            f"[{idx}/{n}] Completed"
        )

    avg_faithfulness = (
        total_faithfulness / n
    )

    hallucination_rate = (
        1 - avg_faithfulness
    )

    print("\n")
    print("=" * 60)
    print("MEDINTEL RAG EVALUATION")
    print("=" * 60)

    print("\nRetrieval")
    print("-" * 60)

    print(
        f"HitRate@5: "
        f"{total_hit / n:.4f}"
    )

    print("\nGeneration")
    print("-" * 60)

    print(
        f"BLEU-1: "
        f"{total_bleu1 / n:.4f}"
    )

    print(
        f"BLEU-2: "
        f"{total_bleu2 / n:.4f}"
    )

    print(
        f"BLEU-4: "
        f"{total_bleu4 / n:.4f}"
    )

    print(
        f"ROUGE-1: "
        f"{total_rouge1 / n:.4f}"
    )

    print(
        f"ROUGE-2: "
        f"{total_rouge2 / n:.4f}"
    )

    print(
        f"ROUGE-L: "
        f"{total_rougeL / n:.4f}"
    )

    print(
        f"BERTScore F1: "
        f"{total_bert / n:.4f}"
    )

    print("\nRAG Metrics")
    print("-" * 60)

    print(
        f"Answer Relevancy: "
        f"{total_answer_rel / n:.4f}"
    )

    print(
        f"Context Relevancy: "
        f"{total_context_rel / n:.4f}"
    )

    print(
        f"Faithfulness: "
        f"{avg_faithfulness:.4f}"
    )

    print(
        f"Hallucination Rate: "
        f"{hallucination_rate:.4f}"
    )

    print("\nPerformance")
    print("-" * 60)

    print(
        f"Average Latency: "
        f"{total_latency / n:.2f} sec"
    )

    print("=" * 60)


if __name__ == "__main__":
    evaluate()