import json

from app.retrieval.embeddings import embed_texts
from app.retrieval.vector_store import collection

BATCH_SIZE = 128


def load_chunks():

    with open(
        "data/processed/chunks.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def main():

    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks")

    existing = collection.count()

    if existing > 0:
        print(
            f"Collection already contains {existing} records"
        )
        print("Delete chroma_store if rebuilding")
        return

    for start in range(
        0,
        len(chunks),
        BATCH_SIZE
    ):

        batch = chunks[
            start:start + BATCH_SIZE
        ]

        docs = [
            c["text"]
            for c in batch
        ]

        embeddings = embed_texts(docs)

        collection.add(
            ids=[
                c["chunk_id"]
                for c in batch
            ],
            documents=docs,
            embeddings=embeddings.tolist(),
            metadatas=[
                {
                    "book": c["book"],
                    "page": c["page"]
                }
                for c in batch
            ]
        )

        print(
            f"Indexed {min(start+BATCH_SIZE,len(chunks))}/{len(chunks)}"
        )

    print("Index build completed")


if __name__ == "__main__":
    main()