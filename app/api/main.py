from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.pipeline import ask

app = FastAPI(
    title="MedIntel API"
)

class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(data: QueryRequest):

    result = ask(data.question)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }