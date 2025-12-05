# app/main.py

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .database import init_db
from .routers import feedback, testruns

# Load variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI(
    title="AI Test Analytics Hub API",
    version="0.1.0",
)

# CORS – allow your front-end origins
origins = [
    "http://localhost:3000",
    "http://localhost:8501",
    "http://127.0.0.1:3000",
    # add your real UI domain later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- API KEY GUARD --------
def verify_api_key(x_api_key: str = Header(None)):
    if API_KEY is None:
        # Misconfiguration: .env missing API_KEY or load_dotenv not working
        raise HTTPException(
            status_code=500,
            detail="API key not configured on server",
        )
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# -------- DB INIT ON STARTUP --------
init_db()

# -------- ROOT --------
@app.get("/")
def read_root():
    return {"message": "AI Test Analytics Hub API is running"}

# -------- ROUTERS (protected by API key) --------
app.include_router(
    feedback.router,
    dependencies=[Depends(verify_api_key)],
)

app.include_router(
    testruns.router,
    dependencies=[Depends(verify_api_key)],
)
