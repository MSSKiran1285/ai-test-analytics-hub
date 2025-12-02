# app/schemas.py

from datetime import datetime
from pydantic import BaseModel


class FeedbackBase(BaseModel):
    user_id: str | None = None
    message: str


class FeedbackCreate(FeedbackBase):
    """Payload for creating feedback."""
    pass


class FeedbackRead(FeedbackBase):
    """What we return to the client."""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
