from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, SystemMessage
from database.db import SessionLocal
from database.models import User
from app.agents.graph import app_graph

app = FastAPI(title="My Banker API")

class QuestionRequest(BaseModel):
    question: str
    user_id: int = 1

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/ask")
async def ask_banker(request: QuestionRequest, db: Session = Depends(get_db)):
    # 1. אימות המשתמש (בדיקה שהוא קיים ב-DB לפני שמתחילים)
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. הגדרת ה-System Prompt (ההנחיות הכלליות)
    # שים לב: אנחנו לא מזריקים פה את כל הטרנזקציות, כי הסוכן ימשוך אותן עם הכלי get_user_balance_tool במידת הצורך
    system_instructions = SystemMessage(content=(
        f"אתה עוזר בנקאי אישי בשם 'My Banker'. המשתמש הוא {user.name} (ID: {user.id}).\n"
        "חוק בל יעבור: לפני שאתה נותן המלצה על סכומי חיסכון, השקעות או ניהול תקציב, "
        "עליך חובה להשתמש בכלי 'get_user_balance_tool' כדי לראות את המצב הפיננסי האמיתי.\n"
        "אל תענה תשובות כלליות אם יש לך אפשרות לבסס אותן על נתוני המשתמש והידע המקצועי ב-RAG."
    ))

    # 3. הכנת המצב הראשוני עבור LangGraph
    # אנחנו מעבירים את ה-user_id בתוך ה-config כדי שהכלים יוכלו להשתמש בו
    initial_state = {
        "messages": [system_instructions, HumanMessage(content=request.question)],
        "user_info": {"id": user.id, "name": user.name},
        "retrieved_context": []
    }
    
    config = {"configurable": {"user_id": user.id}}

    try:
        # 4. הרצת הגרף (אסינכרוני)
        result = await app_graph.ainvoke(initial_state, config=config)
        
        # 5. שליפת התשובה הסופית
        final_message = result["messages"][-1]
        
        return {
            "answer": final_message.content,
            "user_id": user.id,
            # כאן תוכל לראות אילו כלים הופעלו בדרך
            "logic_steps": [m.type for m in result["messages"]] 
        }
    except Exception as e:
        print(f"Error running LangGraph: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/")
def read_root():
    return {"message": "Welcome to the My Banker API"}

@app.get("/users")
def get_users():
    db = next(get_db())
    users = db.query(User).all()
    return users