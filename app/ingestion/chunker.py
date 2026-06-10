from typing import List
from pydantic import BaseModel
from app.utils.text_cleaner import clean_text


class Chunk(BaseModel):
    chunk_id: str
    book: str
    page: int
    text: str


def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 100
):
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def create_chunks(documents):
    all_chunks = []

    chunk_counter = 1

    for doc in documents:

        text = clean_text(doc["text"])

        text_chunks = chunk_text(text)

        for chunk in text_chunks:

            if len(chunk.split()) < 50:
                continue

            all_chunks.append(
                Chunk(
                    chunk_id=f"chunk_{chunk_counter}",
                    book=doc["book"],
                    page=doc["page"],
                    text=chunk
                ).model_dump()
            )

            chunk_counter += 1

    return all_chunks
    all_chunks = []

    chunk_counter = 1

    for doc in documents:

        text_chunks = chunk_text(doc["text"])

        for chunk in text_chunks:

            if len(chunk.split()) < 50:
                continue

            all_chunks.append(
                Chunk(
                    chunk_id=f"chunk_{chunk_counter}",
                    book=doc["book"],
                    page=doc["page"],
                    text=chunk
                ).model_dump()
            )

            chunk_counter += 1

    return all_chunks