from app.core.openai_client import client

class EmbeddingService:

    MODEL = "text-embedding-3-small"

    @staticmethod
    def create_embedding(text: str) -> list[float]:
        response = client.embeddings.create(
            model=EmbeddingService.MODEL,
            input=text
        )
        return response.data[0].embedding
