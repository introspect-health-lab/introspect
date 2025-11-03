from fastapi import FastAPI
from src.auth.controller import router as auth_router
from src.users.controller import router as users_router
from src.patients.controller import router as patients_router
from src.results.controller import router as results_router
from src.dashboard.controller import router as dashboard_router
from src.clinics.controller import router as clinics_router
from src.sync.controller import router as sync_router

def register_routes(app: FastAPI):
    # Authentication routes
    app.include_router(auth_router)

    # Core API routes
    app.include_router(users_router)
    app.include_router(clinics_router)
    app.include_router(patients_router)
    app.include_router(results_router)
    app.include_router(dashboard_router)
    app.include_router(sync_router)