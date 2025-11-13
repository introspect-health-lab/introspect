from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database.core import engine, Base
# Import all entities to register them with SQLAlchemy
from .entities.user import User
from .entities.clinic import Clinic
from .entities.patient import Patient
from .entities.test_result import TestResult
from .api import register_routes
from .app_logging import configure_logging, LogLevels
from .frontend.controller import router as frontend_router
from pathlib import Path


configure_logging(LogLevels.info)

app = FastAPI(
    title="introspect - Malaria Diagnostics API",
    description="API for malaria diagnostics and surveillance using AI-powered blood smear analysis",
    version="1.0.0"
)

# Configure CORS for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" Create tables if they don't exist (for SQLite and local development) """
Base.metadata.create_all(bind=engine)

# Mount static files
static_dir = Path(__file__).parent / "frontend" / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Register API routes
register_routes(app)

# Register frontend routes (should be last to avoid conflicts)
app.include_router(frontend_router)