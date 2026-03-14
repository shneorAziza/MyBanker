from datetime import date
from database.db import SessionLocal, engine, Base
from database.models import User, Transaction
from datetime import datetime

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 1. יצירת משתמשים
yossi = User(name="יוסי", email="yossi@test.com")
dana = User(name="דנה", email="dana@test.com")
db.add_all([yossi, dana])
db.commit()

# 2. טרנזקציות ליוסי (ID: 1) - מצב מעולה
db.add_all([
    Transaction(user_id=yossi.id, amount=20000, category="Salary", description="משכורת הייטק", date=datetime.now()),
    Transaction(user_id=yossi.id, amount=-1500, category="Rent", description="שכר דירה", date=datetime.now()),
    Transaction(user_id=yossi.id, amount=-500, category="Food", description="סופר", date=datetime.now()),
])

# 3. טרנזקציות לדנה (ID: 2) - מצב בעייתי
db.add_all([
    Transaction(user_id=dana.id, amount=6000, category="Salary", description="משכורת חלקית", date=datetime.now()),
    Transaction(user_id=dana.id, amount=-4000, category="Shopping", description="קניון ומותגים", date=datetime.now()),
    Transaction(user_id=dana.id, amount=-2500, category="Entertainment", description="מסעדות יוקרה", date=datetime.now()),
])

db.commit()
db.close()
print("Database re-seeded successfully with 2 distinct users!")