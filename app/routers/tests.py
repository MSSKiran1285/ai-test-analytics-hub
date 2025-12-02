from fastapi import APIRouter

router = APIRouter(prefix="/tests")

@router.get("/")
def tests_home():
    return {"message": "Tests router working"}
