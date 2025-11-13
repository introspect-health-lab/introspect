from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional
from . import models
from src.entities.test_result import TestResult, TestStatus
from src.entities.patient import Patient
from src.entities.clinic import Clinic
from src.entities.user import User, UserRole
from src.auth.models import TokenData
import logging

def get_dashboard_data(
    current_user: TokenData,
    db: Session,
    days: int = 30,
    district: Optional[str] = None
) -> models.DashboardResponse:
    """
    Get comprehensive dashboard data for malaria surveillance.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        days: Number of days to include in time series (default 30)
        district: Optional district filter
    """
    # Calculate date range
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    
    # Base query
    base_query = db.query(TestResult)
    if district:
        base_query = base_query.join(Clinic).filter(Clinic.district == district)
    
    # Get summary statistics
    total_tests = base_query.count()
    
    positive_count = base_query.filter(TestResult.result == TestStatus.Positive).count()
    negative_count = base_query.filter(TestResult.result == TestStatus.Negative).count()
    inconclusive_count = base_query.filter(TestResult.result == TestStatus.Inconclusive).count()
    
    overall_positivity_rate = (positive_count / total_tests * 100) if total_tests > 0 else 0.0
    
    # Get counts
    total_patients = db.query(Patient).count()
    total_clinics = db.query(Clinic).count()
    total_health_workers = db.query(User).filter(User.role == UserRole.HealthWorker).count()
    
    summary = models.DashboardSummary(
        total_tests=total_tests,
        total_positive=positive_count,
        total_negative=negative_count,
        total_inconclusive=inconclusive_count,
        overall_positivity_rate=round(overall_positivity_rate, 2),
        total_patients=total_patients,
        total_clinics=total_clinics,
        total_health_workers=total_health_workers,
        last_updated=datetime.now(timezone.utc)
    )
    
    # Get district statistics
    district_stats = get_district_statistics(db, district)
    
    # Get recent tests count (last 7 days)
    recent_date = end_date - timedelta(days=7)
    recent_tests = base_query.filter(TestResult.test_date >= recent_date).count()
    
    # Get time series data
    time_series = get_time_series_data(db, days, district)
    
    logging.info(f"Generated dashboard data for user {current_user.get_uuid()}")
    
    return models.DashboardResponse(
        summary=summary,
        district_stats=district_stats,
        recent_tests=recent_tests,
        time_series=time_series
    )


def get_district_statistics(db: Session, district_filter: Optional[str] = None) -> List[models.DistrictStats]:
    """Get statistics grouped by district."""
    query = db.query(
        Clinic.district,
        func.count(TestResult.id).label('total_tests'),
        func.sum(case((TestResult.result == TestStatus.Positive, 1), else_=0)).label('positive_cases'),
        func.sum(case((TestResult.result == TestStatus.Negative, 1), else_=0)).label('negative_cases'),
        func.sum(case((TestResult.result == TestStatus.Inconclusive, 1), else_=0)).label('inconclusive_cases'),
        func.count(func.distinct(Clinic.id)).label('clinics_count')
    ).join(TestResult, Clinic.id == TestResult.clinic_id).group_by(Clinic.district)
    
    if district_filter:
        query = query.filter(Clinic.district == district_filter)
    
    results = query.all()
    
    district_stats = []
    for row in results:
        positivity_rate = (row.positive_cases / row.total_tests * 100) if row.total_tests > 0 else 0.0
        district_stats.append(models.DistrictStats(
            district=row.district,
            total_tests=row.total_tests,
            positive_cases=row.positive_cases,
            negative_cases=row.negative_cases,
            inconclusive_cases=row.inconclusive_cases,
            positivity_rate=round(positivity_rate, 2),
            clinics_count=row.clinics_count
        ))
    
    return district_stats


def get_clinic_statistics(db: Session, district: Optional[str] = None) -> List[models.ClinicStats]:
    """Get statistics grouped by clinic."""
    query = db.query(
        Clinic.id,
        Clinic.name,
        Clinic.district,
        func.count(TestResult.id).label('total_tests'),
        func.sum(case((TestResult.result == TestStatus.Positive, 1), else_=0)).label('positive_cases'),
        func.sum(case((TestResult.result == TestStatus.Negative, 1), else_=0)).label('negative_cases'),
        func.sum(case((TestResult.result == TestStatus.Inconclusive, 1), else_=0)).label('inconclusive_cases'),
    ).join(TestResult, Clinic.id == TestResult.clinic_id).group_by(Clinic.id, Clinic.name, Clinic.district)
    
    if district:
        query = query.filter(Clinic.district == district)
    
    results = query.all()
    
    clinic_stats = []
    for row in results:
        positivity_rate = (row.positive_cases / row.total_tests * 100) if row.total_tests > 0 else 0.0
        clinic_stats.append(models.ClinicStats(
            clinic_id=str(row.id),
            clinic_name=row.name,
            district=row.district,
            total_tests=row.total_tests,
            positive_cases=row.positive_cases,
            negative_cases=row.negative_cases,
            inconclusive_cases=row.inconclusive_cases,
            positivity_rate=round(positivity_rate, 2)
        ))
    
    return clinic_stats


def get_time_series_data(db: Session, days: int = 30, district: Optional[str] = None) -> List[models.TimeSeriesData]:
    """Get time series data for the specified number of days."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    
    # Query for daily aggregates
    query = db.query(
        func.date(TestResult.test_date).label('date'),
        func.sum(case((TestResult.result == TestStatus.Positive, 1), else_=0)).label('positive_cases'),
        func.sum(case((TestResult.result == TestStatus.Negative, 1), else_=0)).label('negative_cases'),
        func.count(TestResult.id).label('total_tests')
    ).filter(TestResult.test_date >= start_date)
    
    if district:
        query = query.join(Clinic).filter(Clinic.district == district)
    
    query = query.group_by(func.date(TestResult.test_date)).order_by(func.date(TestResult.test_date))
    
    results = query.all()

    time_series = []
    for row in results:
        # row.date is already a string from func.date() in SQLite
        date_str = row.date if isinstance(row.date, str) else row.date.strftime('%Y-%m-%d')
        time_series.append(models.TimeSeriesData(
            date=date_str,
            positive_cases=row.positive_cases,
            negative_cases=row.negative_cases,
            total_tests=row.total_tests
        ))

    return time_series

