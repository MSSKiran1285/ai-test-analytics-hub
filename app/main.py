# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .database import init_db
from .routers import feedback, testruns
from .dependencies import get_api_key  # our API-key dependency


# Load environment variables from .env (APP_NAME, APP_ENV, API_KEY, etc.)
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "AI Test Analytics Hub API")
APP_ENV = os.getenv("APP_ENV", "dev")

app = FastAPI(
    title=APP_NAME,
    version="0.1.0",
)

# --- CORS setup (for UI / Postman / other clients) ---
origins = ["*"]  # later we can restrict this

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB init on startup ---
init_db()


# --- Health / root endpoint ---
@app.get("/")
def read_root():
    return {"message": f"{APP_NAME} is running in {APP_ENV} mode"}


# --- Routers with API-key protection ---
app.include_router(
    feedback.router,
    dependencies=[Depends(get_api_key)],
)

app.include_router(
    testruns.router,
    dependencies=[Depends(get_api_key)],
)
