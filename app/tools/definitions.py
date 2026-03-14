# app/tools/definitions.py
from langchain_core.tools import tool
from app.tools.rag_tool import search_financial_knowledge as rag_search
from database.db import SessionLocal
from database.models import Transaction, User

@tool
def financial_knowledge_tool(query: str):
    """חיפוש מידע פיננסי מקצועי, חוקים, ריביות וטיפים לחיסכון. השתמש בכלי זה כשעולה שאלה על חסכון, ריבית, או חוקים."""
    results = rag_search(query)
    # חשוב להחזיר סטרינג נקי שה-LLM יכול לקרוא בקלות
    return "\n".join([f"- {res.content}" for res in results])

@tool
def get_user_balance_tool(user_id: int):
    """
    שליפת יתרה ועסקאות. חובה להשתמש בכלי זה לכל שאלה שנוגעת לייעוץ פיננסי, 
    יכולת חיסכון, או ניתוח מצב חשבון.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return "שגיאה: משתמש לא נמצא."
            
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
        balance = sum(t.amount for t in transactions)
        return f"המשתמש הוא {user.name}. היתרה הנוכחית היא: {balance} ש\"ח."
    finally:
        db.close()

# רשימת הכלים שתיוצא לגרף
financial_tools = [financial_knowledge_tool, get_user_balance_tool]