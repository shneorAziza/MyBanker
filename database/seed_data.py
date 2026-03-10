from datetime import date
from database.db import SessionLocal, engine, Base
from database.models import User, Transaction

Base.metadata.create_all(bind=engine)

session = SessionLocal()

# Example user
user = User(name="Shneor Aziza", email="shneor@example.com")
session.add(user)
session.commit()

# Example transactions for the user
transactions = [
    Transaction(user_id=user.id, amount=15000, category="salary", description="March salary", date=date(2026,3,1)),
    Transaction(user_id=user.id, amount=-2000, category="groceries", description="Supermarket", date=date(2026,3,5)),
    Transaction(user_id=user.id, amount=-1000, category="entertainment", description="Movies", date=date(2026,3,7)),
    Transaction(user_id=user.id, amount=-3000, category="travel", description="Weekend trip", date=date(2026,3,10)),
]

session.add_all(transactions)
session.commit()
session.close()