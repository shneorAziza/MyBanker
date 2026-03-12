from database.db import SessionLocal
from database.models import FinancialKnowledge
from app.services.embedding_service import EmbeddingService
from database.db import engine, Base 
from sqlalchemy import text 

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

Base.metadata.create_all(bind=engine)

def seed_financial_tips():
    db = SessionLocal()
    tips = [
        {"text": "מומלץ להפריש לפחות 20% מההכנסה החודשית לחיסכון ארוך טווח.", "source": "general_wisdom"},
        {"text": "ריבית הפריים מורכבת מריבית בנק ישראל בתוספת 1.5%.", "source": "bank_rules"},
        {"text": "קרן השתלמות היא אפיק חיסכון פטור ממס לאחר 6 שנים.", "source": "tax_law_il"}
    ]

    for tip in tips:
        vector = EmbeddingService.create_embedding(tip["text"])
        
        knowledge = FinancialKnowledge(
            content=tip["text"],
            embedding=vector,
            source=tip["source"]
        )
        db.add(knowledge)
    
    db.commit()
    db.close()
    print("Successfully seeded financial knowledge!")

if __name__ == "__main__":
    seed_financial_tips()