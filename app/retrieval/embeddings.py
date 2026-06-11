from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5"
)

def embed_texts(texts: list[str]):
    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )