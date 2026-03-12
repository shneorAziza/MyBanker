from app.services.embedding_service import EmbeddingService

text = "Saving 20% of your monthly income is recommended."

vector = EmbeddingService.create_embedding(text)

print(len(vector))
print(vector[:10])