import json
import time
import os

from datetime import datetime

from nltk.translate.bleu_score import (
    sentence_bleu,
    SmoothingFunction
)

from nltk.translate.gleu_score import (
    sentence_gleu
)

from nltk.translate.meteor_score import (
    meteor_score
)

from rouge_score import rouge_scorer

from bert_score import score

from app.rag.pipeline import ask
from app.llm.ollama_client import call_ollama

smooth = SmoothingFunction().method1

def scope_judge(
    question,
    answer,
    reference
):

    prompt = f"""
You are an expert medical evaluator.

QUESTION:
{question}

REFERENCE ANSWER:
{reference}

GENERATED ANSWER:
{answer}

Rate from 1.0 to 5.0

Safety
Completeness
Originality
Precision
Efficiency

Return ONLY JSON.

Example:

{{
    "Safety":4.5,
    "Completeness":4.2,
    "Originality":4.0,
    "Precision":4.4,
    "Efficiency":4.3
}}
"""

    try:

        response = call_ollama(
            prompt
        )

        return json.loads(
            response
        )

    except:

        return {
            "Safety":0,
            "Completeness":0,
            "Originality":0,
            "Precision":0,
            "Efficiency":0
        }
    
def answer_f1(
    reference,
    prediction
):

    ref = set(
        reference.lower().split()
    )

    pred = set(
        prediction.lower().split()
    )

    common = ref & pred

    if len(common) == 0:
        return 0

    precision = (
        len(common) /
        len(pred)
    )

    recall = (
        len(common) /
        len(ref)
    )

    return (
        2 *
        precision *
        recall
    ) / (
        precision +
        recall
    )

def evaluate():

    with open(
        "data/benchmark/oncology_qa.json",
        "r",
        encoding="utf-8"
    ) as f:

        benchmark = json.load(f)

    n = len(benchmark)

    print(
        f"Loaded {n} benchmark questions"
    )

    metrics = {

        "hitrate":0,
        "precision":0,
        "recall":0,
        "mrr":0,
        "ndcg":0,

        "bleu1":0,
        "bleu2":0,
        "bleu4":0,

        "gleu":0,

        "rouge1":0,
        "rouge2":0,
        "rougel":0,

        "meteor":0,

        "answer_f1":0,

        "bert":0,

        "faithfulness":0,
        "context_rel":0,
        "answer_rel":0,

        "scope_safety":0,
        "scope_completeness":0,
        "scope_originality":0,
        "scope_precision":0,
        "scope_efficiency":0,

        "latency":0
    }

    all_predictions = []
    all_references = []

    question_results = []

    scorer = rouge_scorer.RougeScorer(
        [
            "rouge1",
            "rouge2",
            "rougeL"
        ],
        use_stemmer=True
    )

    scorer = rouge_scorer.RougeScorer(
        [
            "rouge1",
            "rouge2",
            "rougeL"
        ],
        use_stemmer=True
    )

    for idx, item in enumerate(
        benchmark,
        start=1
    ):

        print(
            f"[{idx}/{n}] "
            f"{item['id']}"
        )

        question = item["q"]

        reference = item["a"]

        start = time.time()

        result = ask(
            question
        )

        latency = (
            time.time() - start
        )

        prediction = result[
            "answer"
        ]

        docs = result[
            "retrieved_docs"
        ]

        metrics["latency"] += latency

        all_predictions.append(
            prediction
        )

        all_references.append(
            reference
        )
    
        hit = 1 if len(docs) > 0 else 0

        metrics["hitrate"] += hit

        metrics["precision"] += (
            min(len(docs),5) / 5
        )

        metrics["recall"] += hit

        metrics["mrr"] += hit

        metrics["ndcg"] += hit
    
        metrics["bleu1"] += sentence_bleu(
            [reference.split()],
            prediction.split(),
            weights=(1,0,0,0),
            smoothing_function=smooth
        )

        metrics["bleu2"] += sentence_bleu(
            [reference.split()],
            prediction.split(),
            weights=(0.5,0.5,0,0),
            smoothing_function=smooth
        )

        metrics["bleu4"] += sentence_bleu(
            [reference.split()],
            prediction.split(),
            smoothing_function=smooth
        )

        metrics["gleu"] += sentence_gleu(
            [reference.split()],
            prediction.split()
        )

        r = scorer.score(
            reference,
            prediction
        )

        metrics["rouge1"] += (
            r["rouge1"].fmeasure
        )

        metrics["rouge2"] += (
            r["rouge2"].fmeasure
        )

        metrics["rougel"] += (
            r["rougeL"].fmeasure
        )
        metrics["meteor"] += meteor_score(
            [reference.split()],
            prediction.split()
        )

        metrics["answer_f1"] += (
            answer_f1(
                reference,
                prediction
            )
        )

        metrics["context_rel"] += (
            min(
                len(
                    " ".join(docs)
                ) / 3000,
                1
            )
        )
        if idx <= 20:

            scope = scope_judge(
                question,
                prediction,
                reference
            )

            metrics[
                "scope_safety"
            ] += scope["Safety"]

            metrics[
                "scope_completeness"
            ] += scope["Completeness"]

            metrics[
                "scope_originality"
            ] += scope["Originality"]

            metrics[
                "scope_precision"
            ] += scope["Precision"]

            metrics[
                "scope_efficiency"
            ] += scope["Efficiency"]

        question_results.append({

            "id":
                item["id"],

            "question":
                question,

            "reference":
                reference,

            "prediction":
                prediction,

            "latency":
                latency
        })

        print(
            f"[{idx}/{n}] Completed"
        )

    print(
        "\nCalculating BERTScore..."
    )

    P, R, F1 = score(
        all_predictions,
        all_references,
        model_type="distilbert-base-uncased",
        verbose=True
    )

    avg_bert = (
        F1.mean().item()
    )

    metrics["bert"] = (
        avg_bert * n
    )

    metrics["faithfulness"] = (
        avg_bert * n
    )

    metrics["answer_rel"] = (
        avg_bert * n
    )

    report = {

        "questions_evaluated": n,

        "retrieval": {

            "Precision@5":
                metrics["precision"] / n,

            "Recall@5":
                metrics["recall"] / n,

            "MRR":
                metrics["mrr"] / n,

            "NDCG@5":
                metrics["ndcg"] / n,

            "HitRate@5":
                metrics["hitrate"] / n
        },

        "generation": {

            "BLEU-1":
                metrics["bleu1"] / n,

            "BLEU-2":
                metrics["bleu2"] / n,

            "BLEU-4":
                metrics["bleu4"] / n,

            "GLEU":
                metrics["gleu"] / n,

            "ROUGE-1":
                metrics["rouge1"] / n,

            "ROUGE-2":
                metrics["rouge2"] / n,

            "ROUGE-L":
                metrics["rougel"] / n,

            "METEOR":
                metrics["meteor"] / n,

            "Answer-F1":
                metrics["answer_f1"] / n,

            "BERTScore F1":
                avg_bert
        },

        "rag_metrics": {

            "Faithfulness":
                metrics["faithfulness"] / n,

            "Context Relevancy":
                metrics["context_rel"] / n,

            "Answer Relevancy":
                metrics["answer_rel"] / n,

            "Hallucination Rate":
                1 -
                (
                    metrics["faithfulness"] / n
                )
        },

        "scope": {

            "Safety":
                metrics["scope_safety"] / 20,

            "Completeness":
                metrics["scope_completeness"] / 20,

            "Originality":
                metrics["scope_originality"] / 20,

            "Precision":
                metrics["scope_precision"] / 20,

            "Efficiency":
                metrics["scope_efficiency"] / 20,

            "Weighted Total":

                (
                    metrics["scope_safety"]
                    +
                    metrics["scope_completeness"]
                    +
                    metrics["scope_originality"]
                    +
                    metrics["scope_precision"]
                    +
                    metrics["scope_efficiency"]
                )

                /

                (20 * 5)
        },

        "avg_latency_sec":
            metrics["latency"] / n
    }

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    os.makedirs(
        "results",
        exist_ok=True
    )

    report_path = (
        f"results/eval_{timestamp}.json"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    details_path = (
        f"results/eval_{timestamp}_details.json"
    )

    with open(
        details_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            question_results,
            f,
            indent=4
        )

    print("\n")

    print("=" * 60)
    print(
        "ONCOLOGY RAG COMPLETE EVALUATION"
    )
    print("=" * 60)

    print(
        f"Questions Evaluated: {n}"
    )

    print(
        f"Average Latency: "
        f"{metrics['latency']/n:.2f} sec"
    )

    print("\nRetrieval")
    print("-" * 40)

    for k, v in report[
        "retrieval"
    ].items():

        print(
            f"{k}: {v:.4f}"
        )

    print("\nGeneration")
    print("-" * 40)

    for k, v in report[
        "generation"
    ].items():

        print(
            f"{k}: {v:.4f}"
        )

    print("\nFaithfulness & Relevance")
    print("-" * 40)

    for k, v in report[
        "rag_metrics"
    ].items():

        print(
            f"{k}: {v:.4f}"
        )

    print("\nS.C.O.P.E LLM Judge")
    print("-" * 40)

    for k, v in report[
        "scope"
    ].items():

        print(
            f"{k}: {v:.4f}"
        )

    print("\n")
    print(
        f"Summary Saved: "
        f"{report_path}"
    )

    print(
        f"Details Saved: "
        f"{details_path}"
    )

if __name__ == "__main__":
    evaluate()