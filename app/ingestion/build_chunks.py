import json
from pathlib import Path

from app.ingestion.pdf_loader import load_pdfs
from app.ingestion.chunker import create_chunks


PDF_FOLDER = "data/medical_books"
OUTPUT_FILE = "data/processed/chunks.json"


def main():

    print("Loading PDFs...")

    documents = load_pdfs(PDF_FOLDER)

    print(f"Loaded {len(documents)} pages")

    print("Creating chunks...")

    chunks = create_chunks(documents)

    print(f"Generated {len(chunks)} chunks")

    Path("data/processed").mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved chunks to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()