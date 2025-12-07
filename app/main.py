# app/main.py
from fastapi import FastAPI

from .database import init_db
from .routers import feedback, tests

app = FastAPI(
    title="AI Test Analytics Hub API",
    version="0.1.0",
)

init_db()


@app.get("/")
def read_root():
    return {"message": "AI Test Analytics Hub API is running"}


app.include_router(feedback.router)
app.include_router(tests.router)
