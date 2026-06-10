from typing import List
from pydantic import BaseModel
from app.utils.text_cleaner import clean_text

import re


class Chunk(BaseModel):

    chunk_id: str

    book: str

    page: int

    text: str


NOISE_PATTERNS = [
    "exercise",
    "review questions",
    "references",
    "bibliography",
    "index",
    "answer key"
]


def is_noise(text: str):

    text = text.lower()

    return any(
        noise in text
        for noise in NOISE_PATTERNS
    )


def chunk_text(
    text: str,
    chunk_size: int = 150,
    overlap: int = 30
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        start += (
            chunk_size - overlap
        )

    return chunks


def create_chunks(documents):

    all_chunks = []

    chunk_counter = 1

    for doc in documents:

        text = clean_text(
            doc["text"]
        )

        if is_noise(text):
            continue

        text_chunks = chunk_text(
            text
        )

        for chunk in text_chunks:

            if len(chunk.split()) < 50:
                continue

            lower_chunk = chunk.lower()

            if re.match(
                r"^(fig|figure|table)\s+\d+",
                lower_chunk
            ):
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

    print(
        f"Created {len(all_chunks)} chunks"
    )

    return all_chunks