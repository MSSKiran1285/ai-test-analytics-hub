# app/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Float,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=True)   # optional user id
    message = Column(Text, nullable=False)        # feedback message
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TestRun(Base):
    """
    A single execution of a suite, e.g. 'Nightly Regression 2025-12-05'.
    Aggregated totals are stored here for fast dashboard display.
    """
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_name = Column(String(100), nullable=False)          # e.g. "Nightly Regression"
    suite_name = Column(String(100), nullable=True)         # optional logical suite
    environment = Column(String(50), nullable=True)         # e.g. "QA", "PreProd"
    triggered_by = Column(String(50), nullable=True)        # user / pipeline

    status = Column(String(20), nullable=True, index=True)  # passed/failed/running/queued

    total_tests = Column(Integer, nullable=False, default=0)
    passed_tests = Column(Integer, nullable=False, default=0)
    failed_tests = Column(Integer, nullable=False, default=0)

    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    test_cases = relationship(
        "TestCaseResult",
        back_populates="run",
        cascade="all, delete-orphan",
    )
    prediction = relationship(
        "RunPrediction",
        back_populates="run",
        uselist=False,
        cascade="all, delete-orphan",
    )


class TestCaseResult(Base):
    """
    One row per test case executed in a run.
    """
    __tablename__ = "test_case_results"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("test_runs.id"), nullable=False, index=True)

    case_id = Column(String(100), nullable=True)            # external test id
    name = Column(String(200), nullable=True)
    module = Column(String(100), nullable=True)             # SAP module, feature, etc.

    status = Column(String(20), nullable=False)             # passed/failed/blocked/skipped
    duration_ms = Column(Integer, nullable=True)

    severity = Column(String(20), nullable=True)            # Low/Medium/High/Critical
    failure_reason = Column(Text, nullable=True)
    error_type = Column(String(100), nullable=True)         # e.g. "AssertionError"

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    run = relationship("TestRun", back_populates="test_cases")


class RunPrediction(Base):
    """
    Reserved for the AI/ML part: one row per run with model output.
    """
    __tablename__ = "run_predictions"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("test_runs.id"), nullable=False, unique=True)

    risk_score = Column(Float, nullable=False)              # 0.0 - 1.0
    predicted_fail_count = Column(Integer, nullable=True)
    model_version = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    run = relationship("TestRun", back_populates="prediction")
