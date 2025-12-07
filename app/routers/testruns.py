from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models, schemas
from ..dependencies import get_api_key


router = APIRouter(
    prefix="/testruns",
    tags=["Test Runs"],
    dependencies=[Depends(get_api_key)],
)


@router.post(
    "/",
    response_model=schemas.TestRunRead,
    status_code=status.HTTP_201_CREATED,
)
def create_test_run(
    test_run: schemas.TestRunCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new test run.
    """
    db_test_run = models.TestRun(**test_run.model_dump())
    db.add(db_test_run)
    db.commit()
    db.refresh(db_test_run)
    return db_test_run


@router.get(
    "/",
    response_model=List[schemas.TestRunRead],
)
def list_test_runs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """
    List test runs ordered by most recent first.
    """
    return (
        db.query(models.TestRun)
        .order_by(models.TestRun.executed_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get(
    "/summary",
    response_model=schemas.TestRunSummary,
)
def get_test_run_summary(
    db: Session = Depends(get_db),
):
    """
    Return aggregated stats across all test runs.
    """
    total_runs, total_tests, total_passed, total_failed = (
        db.query(
            func.count(models.TestRun.id),
            func.coalesce(func.sum(models.TestRun.total_tests), 0),
            func.coalesce(func.sum(models.TestRun.passed_tests), 0),
            func.coalesce(func.sum(models.TestRun.failed_tests), 0),
        )
        .one()
    )

    pass_rate = (
        float(total_passed) / total_tests * 100 if total_tests > 0 else 0.0
    )

    return schemas.TestRunSummary(
        total_runs=total_runs,
        total_tests=total_tests,
        total_passed=total_passed,
        total_failed=total_failed,
        pass_rate=pass_rate,
    )

