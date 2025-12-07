# app/routers/tests.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/tests",
    tags=["Test Runs"],
)


# Helper: derive run-level status string for the UI
def derive_run_status(run: models.TestRun) -> str:
    """
    Normalize status for the frontend.

    Returns one of: "passed", "failed", "running", "queued".
    """
    # if explicitly set, normalise and return
    if run.status:
        return run.status.lower()

    # otherwise derive from fields
    if run.started_at is None and run.finished_at is None:
        return "queued"

    if run.finished_at is None:
        return "running"

    # finished -> look at failures
    if run.failed_tests == 0 and run.total_tests > 0:
        return "passed"

    return "failed"


def recompute_aggregates(run: models.TestRun) -> None:
    """
    Update total_tests, passed_tests, failed_tests based on test_cases.
    """
    cases = run.test_cases or []
    total = len(cases)
    passed = sum(1 for c in cases if (c.status or "").lower() == "passed")
    failed = sum(1 for c in cases if (c.status or "").lower() == "failed")

    run.total_tests = total
    run.passed_tests = passed
    run.failed_tests = failed
    run.status = derive_run_status(run)


# ---------- Public Endpoints ----------

@router.get("/", response_model=List[schemas.TestRunRead])
def list_test_runs(db: Session = Depends(get_db)) -> List[schemas.TestRunRead]:
    """
    Returns the list of runs for the dashboard.
    """
    runs = (
        db.query(models.TestRun)
        .order_by(models.TestRun.id.desc())
        .all()
    )

    # ensure status is normalized for the UI
    for r in runs:
        r.status = derive_run_status(r)

    return runs


@router.get("/runs/{run_id}", response_model=schemas.TestRunWithDetails)
def get_run_details(run_id: int, db: Session = Depends(get_db)):
    """
    One run with its test cases + prediction (for drill-down).
    """
    run = (
        db.query(models.TestRun)
        .filter(models.TestRun.id == run_id)
        .first()
    )
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test run not found",
        )

    # normalise aggregates & status before returning
    recompute_aggregates(run)
    db.commit()
    db.refresh(run)

    return run


@router.post("/", response_model=schemas.TestRunRead, status_code=status.HTTP_201_CREATED)
def create_test_run(
    payload: schemas.TestRunCreate,
    db: Session = Depends(get_db),
):
    """
    Create a run header; test cases can be added later.
    """
    run = models.TestRun(**payload.dict())
    db.add(run)
    db.commit()
    db.refresh(run)

    # normalise status for UI
    run.status = derive_run_status(run)
    db.commit()
    db.refresh(run)

    return run


@router.post(
    "/runs/{run_id}/cases",
    response_model=List[schemas.TestCaseResultRead],
    status_code=status.HTTP_201_CREATED,
)
def add_test_cases(
    run_id: int,
    cases: List[schemas.TestCaseResultBase],
    db: Session = Depends(get_db),
):
    """
    Bulk insert test case results for a run (called by your automation).
    """
    run = (
        db.query(models.TestRun)
        .filter(models.TestRun.id == run_id)
        .first()
    )
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test run not found",
        )

    created_rows: list[models.TestCaseResult] = []

    for c in cases:
        row = models.TestCaseResult(run_id=run_id, **c.dict())
        db.add(row)
        created_rows.append(row)

    db.commit()

    # refresh all created rows
    for row in created_rows:
        db.refresh(row)

    # recompute aggregates and normalise status
    recompute_aggregates(run)
    db.commit()
    db.refresh(run)

    return created_rows
