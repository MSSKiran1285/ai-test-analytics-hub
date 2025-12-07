# app/schemas.py
from datetime import datetime
from pydantic import BaseModel

# ---------- Feedback ----------

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


# ---------- Tests & ML ----------

class TestCaseResultBase(BaseModel):
    case_id: str | None = None
    name: str | None = None
    module: str | None = None
    status: str                                   # passed/failed/etc.
    duration_ms: int | None = None
    severity: str | None = None
    failure_reason: str | None = None
    error_type: str | None = None


class TestCaseResultCreate(TestCaseResultBase):
    run_id: int


class TestCaseResultRead(TestCaseResultBase):
    id: int
    run_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RunPredictionRead(BaseModel):
    id: int
    run_id: int
    risk_score: float
    predicted_fail_count: int | None = None
    model_version: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True


class TestRunBase(BaseModel):
    run_name: str
    suite_name: str | None = None
    environment: str | None = None
    triggered_by: str | None = None
    status: str | None = None
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    started_at: datetime | None = None
    finished_at: datetime | None = None


class TestRunCreate(TestRunBase):
    pass


class TestRunRead(TestRunBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TestRunWithDetails(TestRunRead):
    test_cases: list[TestCaseResultRead] = []
    prediction: RunPredictionRead | None = None
