# MedIntel: Agentic Medical Oncology RAG System

## Overview

MedIntel is an Agentic Retrieval-Augmented Generation (RAG) system designed for oncology-focused medical question answering. The system combines hybrid retrieval, agent-based reasoning, reinforcement learning feedback, and automated evaluation to generate evidence-grounded medical responses from trusted oncology literature.

The goal of MedIntel is to provide:

* Accurate oncology information retrieval
* Evidence-grounded answer generation
* Reduced hallucinations
* Explainable retrieval pipelines
* Continuous improvement through feedback and reinforcement learning

---

# Architecture

```text
User Question
      │
      ▼
Query Analyzer Agent
      │
      ▼
Query Expansion Agent
      │
      ▼
Retrieval Planner Agent (RL Assisted)
      │
      ▼
Hybrid Retrieval
 ├── BM25 Search
 └── Semantic Search
      │
      ▼
Cross Encoder Reranker
      │
      ▼
Response Optimizer Agent
      │
      ▼
Evidence Verifier Agent
      │
      ▼
LLM Generator
      │
      ▼
Reflection Agent
      │
      ▼
Confidence Agent
      │
      ▼
Final Answer
```

---

# Agentic Components

## Query Analyzer Agent

Analyzes incoming questions and extracts:

* Intent
* Entities
* Complexity
* Emotion

Example:

```json
{
  "intent": "prognosis",
  "entities": ["lung cancer"],
  "complexity": "moderate",
  "emotion": "neutral"
}
```

Supported intents:

* Diagnosis
* Treatment
* Prognosis
* Prevention
* Side Effects
* Support
* General

---

## Query Expansion Agent

Expands user questions with oncology-specific terminology.

Example:

```text
What is breast cancer?

↓

What is breast cancer?
breast cancer diagnosis staging classification pathology
```

---

## Retrieval Planner Agent

Dynamically adjusts retrieval parameters based on:

* Intent
* Complexity
* Emotion
* Reinforcement Learning feedback

Example plan:

```json
{
  "bm25_k": 20,
  "semantic_k": 25,
  "candidate_pool": 40,
  "rerank_top_k": 16
}
```

---

## Response Optimizer Agent

Improves retrieval quality through:

* Duplicate removal
* Chunk ranking
* Section-aware scoring
* Context trimming
* Table-of-contents filtering

---

## Evidence Verifier Agent

Filters weak evidence before generation.

Verification considers:

* Entity matching
* Intent alignment
* Evidence density
* Context quality

---

## Reflection Agent

Performs self-review of generated answers.

Responsibilities:

* Detect unsupported claims
* Improve grounding
* Refine answer structure
* Reduce hallucinations

---

## Confidence Agent

Estimates answer reliability using:

* Evidence coverage
* Context volume
* Entity coverage
* Grounding quality

Example:

```json
{
  "confidence": 0.91
}
```

---

# Retrieval System

## Hybrid Retrieval

MedIntel combines:

### BM25

Traditional keyword retrieval.

### Semantic Search

Dense vector similarity search.

### Cross Encoder Reranking

Improves ranking quality by scoring query-document relevance.

Current performance:

```text
Recall@5 = 1.00
MRR = 1.00
NDCG@5 = 1.00
```

---

# Data Processing

## Agentic Chunking

Documents are processed into:

* Sections
* Paragraph-aware chunks
* Context-preserving segments

Chunk metadata:

```json
{
  "chunk_id": "...",
  "book": "...",
  "page": 123,
  "section": "Breast Cancer",
  "text": "..."
}
```

---

# Reinforcement Learning Layer

## Feedback Store

Stores user feedback:

```json
{
  "question": "...",
  "intent": "diagnosis",
  "reward": 0.82
}
```

---

## Reward Model

Learns retrieval preferences from feedback.

Example:

```json
{
  "diagnosis": {
    "avg_reward": 0.36,
    "samples": 3
  },
  "prognosis": {
    "avg_reward": 0.82,
    "samples": 1
  }
}
```

Used by:

* Retrieval Planner
* Candidate Pool Selection
* Reranking Depth

---

# Evaluation Framework

## Retrieval Metrics

* Precision@5
* Recall@5
* MRR
* NDCG
* HitRate

---

## Generation Metrics

* BLEU-1
* BLEU-2
* BLEU-4
* GLEU
* ROUGE-1
* ROUGE-2
* ROUGE-L
* METEOR
* Answer F1
* BERTScore

---

## RAG Metrics

* Faithfulness
* Context Relevancy
* Answer Relevancy
* Hallucination Rate

---

## Deep Evaluation (SCOPE)

Automated answer quality assessment.

Dimensions:

### Safety

Medical safety of response.

### Completeness

Coverage of user question.

### Originality

Ability to synthesize information.

### Precision

Specificity and correctness.

### Evidence

Grounding in retrieved sources.

Example:

```json
{
  "Safety": 4.0,
  "Completeness": 4.4,
  "Originality": 2.6,
  "Precision": 4.2,
  "Evidence": 4.2
}
```

---

# Current Benchmark Results

```json
{
  "Precision@5": 0.72,
  "Recall@5": 1.00,
  "MRR": 1.00,
  "NDCG@5": 1.00,

  "BERTScore": 0.853,

  "Faithfulness": 0.853,

  "Hallucination Rate": 0.147,

  "Safety": 4.0,
  "Completeness": 4.4,
  "Precision": 4.2,
  "Evidence": 4.2,

  "Confidence": 0.91
}
```

---

# Technology Stack

## Backend

* Python

## Retrieval

* BM25
* Sentence Transformers
* Cross Encoder Reranker

## LLM

* Ollama
* Qwen Models

## Evaluation

* NLTK
* ROUGE
* BERTScore
* Custom DeepEval

---

# Future Work

* Intent-specific answer templates
* Reflection gating for latency reduction
* Evaluation caching
* Multi-hop reasoning
* Citation generation
* Medical knowledge graph integration
* Production API deployment
* Web UI

---

# Disclaimer

MedIntel is a research and educational system designed for oncology information retrieval and question answering. It is not intended to replace professional medical advice, diagnosis, or treatment.
