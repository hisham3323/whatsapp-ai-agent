from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False) # This will be either 'user' or 'assistant'
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)