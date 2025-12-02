# app/routers/feedback.py

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.get("/", response_model=List[schemas.FeedbackRead])
def list_feedback(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Return recent feedback records."""
    feedback_rows = (
        db.query(models.Feedback)
        .order_by(models.Feedback.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return feedback_rows


@router.post(
    "/",
    response_model=schemas.FeedbackRead,
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(
    payload: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
):
    """Insert a new feedback row into RDS."""
    feedback = models.Feedback(**payload.dict())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
