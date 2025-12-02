# app/main.py

from fastapi import FastAPI

from .database import init_db
from .routers import feedback  # and tests if you have tests router


app = FastAPI(
    title="AI Test Analytics Hub API",
    version="0.1.0",
)

# Create tables on startup (for now, simple approach)
init_db()


@app.get("/")
def read_root():
    return {"message": "AI Test Analytics Hub API is running"}


# Routers
app.include_router(feedback.router)
# app.include_router(tests.router)  # if you have another router
