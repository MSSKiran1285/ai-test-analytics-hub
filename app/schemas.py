# app/schemas.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from pydantic import BaseModel


# -------- Feedback Schemas --------

class FeedbackBase(BaseModel):
    message: str
    user_id: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    """Payload for creating feedback."""
    pass


class FeedbackRead(FeedbackBase):
    """Payload returned to clients."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------- TestRun Schemas --------

class TestRunBase(BaseModel):
    run_name: str
    suite_name: str
    environment: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    execution_time_seconds: Optional[float] = None


class TestRunCreate(TestRunBase):
    """Payload for creating a new test run."""
    pass


class TestRunRead(TestRunBase):
    """Payload returned when reading a test run."""
    id: int
    executed_at: datetime

    class Config:
        from_attributes = True


class TestRunSummary(BaseModel):
    """High-level analytics for test runs."""
    total_runs: int
    total_tests: int
    total_passed: int
    total_failed: int
    average_pass_rate: float
    last_run_at: Optional[datetime] = None

