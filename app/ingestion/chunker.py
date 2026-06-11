from pydantic import BaseModel
from app.utils.text_cleaner import clean_text

from app.ingestion.agentic_chunker import (
    split_into_sections,
    chunk_section
)


class Chunk(BaseModel):

    chunk_id: str
    book: str
    page: int
    section: str
    text: str


def create_chunks(documents):

    all_chunks = []

    chunk_counter = 1

    for doc in documents:

        text = clean_text(
            doc["text"]
        )

        sections = split_into_sections(text)
        if chunk_counter == 1:
            print("\nRAW PAGE TEXT")
            print("=" * 80)
            print(text[:2000])
            print("=" * 80)
        if chunk_counter < 20:
            print("\n" + "="*80)
            print("PAGE:", doc["page"])
            print("FIRST 500 CHARS:")
            print(text[:500])

            print("\nSECTIONS FOUND:")
            for s in sections[:10]:
                print("TITLE:", s[0])

        for section_title, section_text in sections:

            chunks = chunk_section(
                section_text
            )

            for chunk in chunks:

                if len(
                    chunk.split()
                ) < 50:
                    continue

                chunk_text = (
                    f"SECTION: {section_title}\n\n"
                    f"{chunk}"
                )

                all_chunks.append(

                    Chunk(

                        chunk_id=
                        f"chunk_{chunk_counter}",

                        book=
                        doc["book"],

                        page=
                        doc["page"],

                        section=
                        section_title,

                        text=
                        chunk_text

                    ).model_dump()

                )

                chunk_counter += 1

    return all_chunks