from pathlib import Path
import fitz
import logging

logging.basicConfig(level=logging.INFO)

def load_pdfs(pdf_dir: str):
    pdf_path = Path(pdf_dir)

    documents = []

    for pdf_file in pdf_path.glob("*.pdf"):
        try:
            doc = fitz.open(pdf_file)

            for page_num in range(len(doc)):
                page = doc[page_num]

                documents.append(
                    {
                        "book": pdf_file.stem,
                        "page": page_num + 1,
                        "text": page.get_text()
                    }
                )

            logging.info(f"Loaded {pdf_file.name}")

        except Exception as e:
            logging.error(f"Error reading {pdf_file}: {e}")

    return documents