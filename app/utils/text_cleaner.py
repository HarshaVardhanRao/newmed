import re


def clean_text(text: str) -> str:
    text = re.sub(
        r"^\d+\s+Chapter\s+\d+.*?$",
        "",
        text,
        flags=re.MULTILINE
    )

    text = re.sub(
        r"Page\s+\d+",
        "",
        text
    )
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()