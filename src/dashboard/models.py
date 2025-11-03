from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class DistrictStats(BaseModel):
    """Statistics for a specific district."""
    district: str
    total_tests: int
    positive_cases: int
    negative_cases: int
    inconclusive_cases: int
    positivity_rate: float
    clinics_count: int

class ClinicStats(BaseModel):
    """Statistics for a specific clinic."""
    clinic_id: str
    clinic_name: str
    district: str
    total_tests: int
    positive_cases: int
    negative_cases: int
    inconclusive_cases: int
    positivity_rate: float

class TimeSeriesData(BaseModel):
    """Time series data point."""
    date: str
    positive_cases: int
    negative_cases: int
    total_tests: int

class DashboardSummary(BaseModel):
    """Overall dashboard summary."""
    total_tests: int
    total_positive: int
    total_negative: int
    total_inconclusive: int
    overall_positivity_rate: float
    total_patients: int
    total_clinics: int
    total_health_workers: int
    last_updated: datetime

class DashboardResponse(BaseModel):
    """Complete dashboard response."""
    summary: DashboardSummary
    district_stats: List[DistrictStats]
    recent_tests: int
    time_series: List[TimeSeriesData]

