from fastapi import APIRouter

router = APIRouter(prefix="/analytics")

@router.get("/")
def analytics_home():
    return {"message": "Analytics router working"}
