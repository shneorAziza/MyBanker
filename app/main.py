from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import User, Transaction
from app.core.openai_client import client
from app.tools.rag_tool import search_financial_knowledge

app = FastAPI(title="My Banker API")

class QuestionRequest(BaseModel):
    question: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ask")
def ask_banker(request: QuestionRequest, db: Session = Depends(get_db)):
    question = request.question

    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()
    balance = sum(t.amount for t in transactions)
    transactions_summary = "\n".join(
        f"{t.date}: {t.category} {t.amount} ({t.description})" for t in transactions
    )

    rag_results = search_financial_knowledge(question, limit=2)
    context_text = "\n".join(f"{res.source}: {res.content}" for res in rag_results)

    prompt_system = f"""
    אתה עוזר בנקאי אישי מקצועי בשם 'My Banker'.
    פרטי משתמש: {user.name}
    יתרה נוכחית: {balance} ש״ח
    פירוט עסקאות אחרונות:
    {transactions_summary}

    מידע פיננסי רלוונטי לשאלה (השתמש בו כדי לענות בצורה מקצועית):
    {context_text}

    הנחיות:
    - ענה על סמך נתוני המשתמש והמידע הפיננסי שסופק.
    - אם המידע הפיננסי לא רלוונטי ישירות, השתמש בידע הכללי שלך אך ציין זאת.
    - היה תמציתי, מקצועי ומניע לפעולה.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": question}
        ],
        max_tokens=300,
        temperature=0.5
    )
    print("OpenAI query:", prompt_system, question)

    answer = response.choices[0].message.content
    return {
        "answer": answer,
        "context_used": [res.source for res in rag_results]
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the My Banker API"}

@app.get("/users")
def get_users():
    db = next(get_db())
    users = db.query(User).all()
    return users