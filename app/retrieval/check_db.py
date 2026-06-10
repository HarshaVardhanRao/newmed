from app.retrieval.vector_store import collection

print(
    f"Documents in DB: {collection.count()}"
)