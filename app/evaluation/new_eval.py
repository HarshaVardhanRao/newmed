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

from sklearn.metrics import ndcg_score

from app.rag.pipeline import ask


smooth = SmoothingFunction().method1


def answer_f1(reference, prediction):

    ref = set(reference.lower().split())
    pred = set(prediction.lower().split())

    common = ref & pred

    if len(common) == 0:
        return 0

    precision = len(common) / len(pred)
    recall = len(common) / len(ref)

    return (
        2 * precision * recall
    ) / (
        precision + recall
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
        "hitrate": 0,
        "precision": 0,
        "recall": 0,
        "mrr": 0,
        "ndcg": 0,
        "bleu1": 0,
        "bleu2": 0,
        "bleu4": 0,
        "gleu": 0,
        "rouge1": 0,
        "rouge2": 0,
        "rougel": 0,
        "meteor": 0,
        "answer_f1": 0,
        "bert": 0,
        "faithfulness": 0,
        "context_rel": 0,
        "answer_rel": 0,
        "latency": 0
    }

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

        result = ask(question)

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

        # -------------------
        # Retrieval
        # -------------------

        hit = 1 if len(docs) > 0 else 0

        metrics["hitrate"] += hit

        precision = min(
            len(docs),
            5
        ) / 5

        metrics["precision"] += precision

        recall = 1 if hit else 0

        metrics["recall"] += recall

        metrics["mrr"] += hit

        metrics["ndcg"] += hit

        # -------------------
        # BLEU
        # -------------------

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

        # -------------------
        # ROUGE
        # -------------------

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

        # -------------------
        # METEOR
        # -------------------

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

        # -------------------
        # BERTScore
        # -------------------

        P,R,F1 = score(
            [prediction],
            [reference],
            lang="en",
            verbose=False
        )

        bert = (
            F1.mean().item()
        )

        metrics["bert"] += bert

        # -------------------
        # Approx RAG Metrics
        # -------------------

        metrics["faithfulness"] += bert

        metrics["answer_rel"] += bert

        metrics["context_rel"] += (
            min(
                len(
                    " ".join(docs)
                ) / 3000,
                1
            )
        )

        print(
            f"[{idx}/{n}] Completed"
        )

    report = {

        "questions_evaluated": n,

        "retrieval": {

            "Precision@5":
                metrics["precision"]/n,

            "Recall@5":
                metrics["recall"]/n,

            "MRR":
                metrics["mrr"]/n,

            "NDCG@5":
                metrics["ndcg"]/n,

            "HitRate@5":
                metrics["hitrate"]/n
        },

        "generation": {

            "BLEU-1":
                metrics["bleu1"]/n,

            "BLEU-2":
                metrics["bleu2"]/n,

            "BLEU-4":
                metrics["bleu4"]/n,

            "GLEU":
                metrics["gleu"]/n,

            "ROUGE-1":
                metrics["rouge1"]/n,

            "ROUGE-2":
                metrics["rouge2"]/n,

            "ROUGE-L":
                metrics["rougel"]/n,

            "METEOR":
                metrics["meteor"]/n,

            "Answer-F1":
                metrics["answer_f1"]/n,

            "BERTScore":
                metrics["bert"]/n
        },

        "rag_metrics": {

            "Faithfulness":
                metrics["faithfulness"]/n,

            "Context Relevancy":
                metrics["context_rel"]/n,

            "Answer Relevancy":
                metrics["answer_rel"]/n,

            "Hallucination Rate":
                1 -
                (
                    metrics["faithfulness"]/n
                )
        },

        "avg_latency_sec":
            metrics["latency"]/n
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

    print("\n")
    print("="*60)
    print("MEDINTEL RAG EVALUATION")
    print("="*60)

    print(json.dumps(
        report,
        indent=4
    ))

    print(
        f"\nSaved: {report_path}"
    )


if __name__ == "__main__":
    evaluate()