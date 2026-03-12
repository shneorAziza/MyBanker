from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector
from database.db import Base
from sqlalchemy import DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date)
    user = relationship("User", back_populates="transactions")

class FinancialKnowledge(Base):
    __tablename__ = "financial_knowledge"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False) 
    embedding = Column(Vector(1536))      
    source = Column(String)        
    created_at = Column(DateTime, default=datetime.utcnow)     

User.transactions = relationship("Transaction", back_populates="user")