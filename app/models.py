from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func

from .database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=True)
    message = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_name = Column(String(255), nullable=False, index=True)
    suite_name = Column(String(255), nullable=False, index=True)
    environment = Column(String(100), nullable=False)
    total_tests = Column(Integer, nullable=False)
    passed_tests = Column(Integer, nullable=False)
    failed_tests = Column(Integer, nullable=False)
    execution_time_seconds = Column(Float, nullable=False)

    # executed_at will be auto-filled by the DB if not provided
    executed_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

