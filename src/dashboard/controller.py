from fastapi import APIRouter, Query
from typing import Optional, List

from ..database.core import DbSession
from . import models
from . import service
from ..auth.service import CurrentUser

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

@router.get("/", response_model=models.DashboardResponse)
def get_dashboard(
    db: DbSession,
    current_user: CurrentUser,
    days: int = Query(30, description="Number of days for time series data"),
    district: Optional[str] = Query(None, description="Filter by district")
):
    """
    Get comprehensive dashboard data for malaria surveillance.
    Includes summary statistics, district breakdowns, and time series data.
    """
    return service.get_dashboard_data(current_user, db, days, district)


@router.get("/districts", response_model=List[models.DistrictStats])
def get_district_stats(
    db: DbSession,
    current_user: CurrentUser,
    district: Optional[str] = Query(None, description="Filter by specific district")
):
    """Get statistics grouped by district."""
    return service.get_district_statistics(db, district)


@router.get("/clinics", response_model=List[models.ClinicStats])
def get_clinic_stats(
    db: DbSession,
    current_user: CurrentUser,
    district: Optional[str] = Query(None, description="Filter by district")
):
    """Get statistics grouped by clinic."""
    return service.get_clinic_statistics(db, district)

