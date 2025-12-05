from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Dependency: Verify API key
def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

from .database import init_db
from .routers import feedback, testruns

app = FastAPI(
    title="AI Test Analytics Hub API",
    version="0.1.0"
)

# CORS: allow your frontend (update when UI deployed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
init_db()

@app.get("/")
def read_root():
    return {"message": "AI Test Analytics Hub API is running"}

# Routers with API Key enforcement
app.include_router(
    feedback.router,
    dependencies=[Depends(verify_api_key)]
)

app.include_router(
    testruns.router,
    dependencies=[Depends(verify_api_key)]
)
