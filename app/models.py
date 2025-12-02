# app/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=True)   # optional user id
    message = Column(Text, nullable=False)        # feedback message
    created_at = Column(DateTime(timezone=True), server_default=func.now())
