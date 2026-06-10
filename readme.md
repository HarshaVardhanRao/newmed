# MedIntel – Oncology RAG Assistant

## Overview

MedIntel is a Retrieval-Augmented Generation (RAG) system designed for oncology-focused medical question answering. The system combines hybrid retrieval, reranking, and local Large Language Models (LLMs) to provide grounded, source-backed answers from oncology textbooks, clinical guidelines, and medical references.

The objective is to improve answer accuracy, reduce hallucinations, and provide transparent citations for medical information retrieval.

---

## Architecture

```text
User Question
      │
      ▼
Hybrid Retriever
(BM25 + Dense Retrieval)
      │
      ▼
Cross Encoder Reranker
      │
      ▼
Top Relevant Chunks
      │
      ▼
Prompt Construction
      │
      ▼
Local LLM (Ollama)
      │
      ▼
Generated Answer
      │
      ▼
Sources + Evaluation
```

---

## Features

### Retrieval

* BM25 lexical retrieval
* ChromaDB vector search
* BGE embeddings
* Reciprocal Rank Fusion
* Cross-Encoder reranking

### Models

#### Embedding Model

```text
BAAI/bge-small-en-v1.5
```

#### Reranker

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

---

## Generation

Local inference through Ollama.

Supported models:

```text
qwen2.5:1.5b
qwen3:8b
llama3
mistral
```

Current default:

```text
qwen2.5:1.5b
```

---

## Evaluation Metrics

### Retrieval Metrics

* Precision@5
* Recall@5
* MRR
* NDCG@5
* HitRate@5

### Lexical Generation Metrics

* BLEU-1
* BLEU-2
* BLEU-4
* GLEU
* ROUGE-1
* ROUGE-2
* ROUGE-L
* METEOR
* Answer-F1

### Semantic Metrics

* BERTScore F1

### RAG Metrics

* Faithfulness
* Context Relevancy
* Answer Relevancy
* Hallucination Rate

### S.C.O.P.E LLM-as-a-Judge Metrics

* Safety
* Completeness
* Originality
* Precision
* Efficiency

---

## Project Structure

```text
newmed/
│
├── app/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   └── build_chunks.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── bm25_search.py
│   │   └── hybrid_search.py
│   │
│   ├── reranking/
│   │   └── reranker.py
│   │
│   ├── llm/
│   │   ├── prompts.py
│   │   ├── ollama_client.py
│   │   └── generator.py
│   │
│   ├── rag/
│   │   └── pipeline.py
│   │
│   ├── api/
│   │   └── main.py
│   │
│   └── evaluation/
│       └── new_eval.py
│
├── data/
│   ├── books/
│   ├── processed/
│   └── benchmark/
│
├── chroma_db/
├── results/
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## Dataset

Medical sources include:

* Cancer Indian Guidelines
* Basics of Oncology
* MD Anderson Manual of Medical Oncology
* Additional oncology textbooks

Processing pipeline:

1. PDF Extraction
2. Text Cleaning
3. Chunking
4. Embedding Generation
5. ChromaDB Indexing

---

## Chunking Strategy

### Structure-Aware Chunking

Stored metadata:

```json
{
  "book": "Cancer Guidelines",
  "page": 12,
  "section": "Breast Cancer",
  "chunk_id": "chunk_102"
}
```

Configuration:

```text
Chunk Size : 450 words
Overlap    : 75 words
```

Benefits:

* Better retrieval quality
* More accurate citations
* Reduced hallucinations
* Improved reranking

---

## Installation

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Required Packages

```bash
pip install fastapi uvicorn streamlit chromadb sentence-transformers
pip install rank-bm25 transformers torch nltk bert-score
pip install rouge-score scikit-learn pydantic pypdf requests
```

---

## Ollama Setup

Pull model:

```bash
ollama pull qwen2.5:1.5b
```

Start Ollama:

```bash
ollama serve
```

Verify installation:

```bash
ollama list
```

---

## Build Knowledge Base

### Extract and Chunk PDFs

```bash
python -m app.ingestion.build_chunks
```

### Build Vector Database

```bash
python -m app.retrieval.vector_store
```

---

## Run FastAPI Server

```bash
uvicorn app.api.main:app --reload
```

Endpoint:

```text
POST /ask
```

Request:

```json
{
  "question": "What is breast cancer?"
}
```

---

## Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

## Run Evaluation

```bash
python -m app.evaluation.new_eval
```

Outputs:

```text
results/
├── eval_TIMESTAMP.json
└── eval_TIMESTAMP_details.json
```

---

## Example Evaluation Output

```text
============================================================
ONCOLOGY RAG COMPLETE EVALUATION
============================================================

Questions Evaluated: 200

Retrieval
----------------------------------------
Precision@5: 0.6840
Recall@5: 0.9750
MRR: 0.8639
NDCG@5: 0.8895
HitRate@5: 0.9750

Generation
----------------------------------------
BLEU-1: 0.2324
BLEU-2: 0.1389
BLEU-4: 0.0505
GLEU: 0.0957
ROUGE-1: 0.2877
ROUGE-2: 0.1129
ROUGE-L: 0.2267
METEOR: 0.3583
Answer-F1: 0.2309
BERTScore F1: 0.9087

Faithfulness & Relevance
----------------------------------------
Faithfulness: 0.6610
Context Relevancy: 0.5051
Answer Relevancy: 0.6275
Hallucination Rate: 0.3390

S.C.O.P.E LLM Judge
----------------------------------------
Safety: 3.49
Completeness: 3.96
Originality: 3.95
Precision: 3.92
Efficiency: 3.90
Weighted Total: 3.80
```

---

## Future Improvements

* Knowledge Graph RAG
* Agentic RAG
* Query Rewriting
* Multi-hop Retrieval
* Medical NER
* Citation Highlighting
* Quantized GPU Models
* Fine-Tuned Medical LLMs
* Clinical Trial Retrieval
* Drug Interaction Analysis

---

## Author

**Harsha Vardhan Rao**

Medical AI • Retrieval-Augmented Generation • FastAPI • NLP • LLM Engineering

**Project:** MedIntel – Oncology Retrieval-Augmented Generation System
