from pathlib import Path

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from .database import init_db

from .routes import router


# ---------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description=(
        "AI-powered personalized fitness plan "
        "generator using Google Gemini."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
)


# ---------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------

STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static"
)


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

app.include_router(
    router
)


# ---------------------------------------------------------
# STARTUP
# ---------------------------------------------------------

@app.on_event("startup")
def startup_event():

    init_db()


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "application": "FitBuddy",
        "version": "1.0.0"
    }