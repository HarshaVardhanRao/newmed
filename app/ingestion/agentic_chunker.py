import re


SECTION_PATTERNS = [

    r"^chapter\s+\d+",

    r"^\d+\.",

    r"^\d+\.\d+",

    r"^[A-Z][A-Z\s\-]{5,}$",

    r"^(introduction|diagnosis|treatment|management|prognosis|epidemiology|risk factors)$"

]


def is_heading(line: str):

    line = line.strip()

    if len(line) < 3:
        return False

    for pattern in SECTION_PATTERNS:

        if re.match(
            pattern,
            line,
            re.IGNORECASE
        ):
            return True

    if (
        len(line.split()) <= 10
        and line.isupper()
    ):
        return True

    return False


def split_into_sections(text):

    lines = text.split("\n")

    sections = []

    current_section = []

    for line in lines:

        if is_heading(line):

            if current_section:

                sections.append(
                    "\n".join(
                        current_section
                    )
                )

            current_section = [line]

        else:

            current_section.append(
                line
            )

    if current_section:

        sections.append(
            "\n".join(
                current_section
            )
        )

    return sections


def chunk_section(section):

    paragraphs = [
        p.strip()
        for p in section.split("\n\n")
        if len(p.strip()) > 50
    ]

    chunks = []

    current = ""

    for para in paragraphs:

        if len(current) + len(para) < 1500:

            current += "\n\n" + para

        else:

            chunks.append(current)

            current = para

    if current:
        chunks.append(current)

    return chunks