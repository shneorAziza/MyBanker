from sqlalchemy import text
from database.db import SessionLocal
from app.services.embedding_service import EmbeddingService
from sqlalchemy import text
from database.db import SessionLocal
from app.services.embedding_service import EmbeddingService

def search_financial_knowledge(query: str, limit: int = 3):
    query_embedding = EmbeddingService.create_embedding(query)
    
    db = SessionLocal()
    try:
        statement = text("""
            SELECT content, source
            FROM financial_knowledge
            ORDER BY embedding <=> :embedding
            LIMIT :limit
        """)
        
        results = db.execute(statement, {
            "embedding": str(query_embedding),
            "limit": limit
        }).fetchall()
        
        return results
    finally:
        db.close()