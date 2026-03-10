from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database.db import SessionLocal
from database.models import User, Transaction
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="My Banker API")

class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_banker(request: QuestionRequest):
    question = request.question

    db = next(get_db())
    user = db.query(User).first()
    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()

    balance = sum(t.amount for t in transactions)
    transactions_summary = "\n".join(
        f"{t.date}: {t.category} {t.amount} ({t.description})" for t in transactions
    )

    prompt_system = f"""
אתה עוזר בנקאי אישי בשם 'My Banker'.
המשתמש: {user.name}
סכום נוכחי: {balance} ש״ח
טרנזקציות אחרונות:
{transactions_summary}
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": question}
        ],
        max_tokens=300,
        temperature=0.7
    )
    print("OpenAI query:", prompt_system, question)

    answer = response.choices[0].message.content
    return {"answer": answer}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the My Banker API"}

@app.get("/users")
def get_users():
    db = next(get_db())
    users = db.query(User).all()
    return users