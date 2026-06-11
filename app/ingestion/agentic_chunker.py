import re


def split_into_sections(text):

    text = text.strip()

    if not text:
        return [
            ("GENERAL", "")
        ]

    first_line = text[:200]

    match = re.match(
        r"^([A-Z][A-Za-z0-9\s\-\(\)]{5,80})",
        first_line
    )

    if match:

        title = match.group(1).strip()

    else:

        title = " ".join(
            text.split()[:10]
        )

    return [
        (
            title,
            text
        )
    ]

def chunk_section(
    section_text,
    max_chars=1800
):

    paragraphs = [

        p.strip()

        for p in re.split(
            r"\n\s*\n",
            section_text
        )

        if len(p.strip()) > 50

    ]

    chunks = []

    current = ""

    for para in paragraphs:

        if (
            len(current)
            + len(para)
        ) < max_chars:

            current += (
                "\n\n" + para
            )

        else:

            chunks.append(
                current.strip()
            )

            current = para

    if current:

        chunks.append(
            current.strip()
        )

    return chunks