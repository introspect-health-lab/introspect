import pytest
from uuid import uuid4
from sqlalchemy.orm import Session
from src.clinics import service, models
from src.entities.clinic import Clinic
from src.auth.models import TokenData
from src.exceptions import ClinicNotFoundError

@pytest.fixture
def test_user():
    """Create a test user token."""
    return TokenData(user_id=str(uuid4()))

@pytest.fixture
def test_clinic(db_session: Session):
    """Create a test clinic."""
    clinic = Clinic(
        id=uuid4(),
        name="Central Health Clinic",
        district="Gaborone",
        region="South-East",
        latitude=-24.6282,
        longitude=25.9231,
        contact_phone="+267 1234567"
    )
    db_session.add(clinic)
    db_session.commit()
    db_session.refresh(clinic)
    return clinic

def test_create_clinic(db_session: Session, test_user: TokenData):
    """Test creating a new clinic."""
    clinic_data = models.ClinicCreate(
        name="New Health Center",
        district="Francistown",
        region="North-East",
        latitude=-21.1699,
        longitude=27.5084,
        contact_phone="+267 2468000",
        contact_email="clinic@example.com"
    )
    
    clinic = service.create_clinic(test_user, db_session, clinic_data)
    
    assert clinic.id is not None
    assert clinic.name == "New Health Center"
    assert clinic.district == "Francistown"
    assert clinic.region == "North-East"
    assert clinic.latitude == -21.1699

def test_get_clinics(db_session: Session, test_user: TokenData, test_clinic: Clinic):
    """Test retrieving all clinics."""
    clinics = service.get_clinics(test_user, db_session)
    
    assert len(clinics) >= 1
    assert any(c.id == test_clinic.id for c in clinics)

def test_get_clinic_by_id(db_session: Session, test_user: TokenData, test_clinic: Clinic):
    """Test retrieving a clinic by ID."""
    clinic = service.get_clinic_by_id(test_user, db_session, test_clinic.id)
    
    assert clinic.id == test_clinic.id
    assert clinic.name == test_clinic.name
    assert clinic.district == test_clinic.district

def test_get_clinic_by_id_not_found(db_session: Session, test_user: TokenData):
    """Test retrieving a non-existent clinic."""
    with pytest.raises(ClinicNotFoundError):
        service.get_clinic_by_id(test_user, db_session, uuid4())

def test_update_clinic(db_session: Session, test_user: TokenData, test_clinic: Clinic):
    """Test updating a clinic."""
    update_data = models.ClinicUpdate(
        contact_phone="+267 7654321",
        contact_email="updated@example.com"
    )
    
    updated_clinic = service.update_clinic(test_user, db_session, test_clinic.id, update_data)
    
    assert updated_clinic.contact_phone == "+267 7654321"
    assert updated_clinic.contact_email == "updated@example.com"
    assert updated_clinic.name == test_clinic.name  # Unchanged

def test_delete_clinic(db_session: Session, test_user: TokenData, test_clinic: Clinic):
    """Test deleting a clinic."""
    clinic_id = test_clinic.id
    
    service.delete_clinic(test_user, db_session, clinic_id)
    
    with pytest.raises(ClinicNotFoundError):
        service.get_clinic_by_id(test_user, db_session, clinic_id)

def test_get_clinics_filtered_by_district(db_session: Session, test_user: TokenData):
    """Test filtering clinics by district."""
    # Create clinics in different districts
    clinic1 = Clinic(
        id=uuid4(),
        name="Gaborone Clinic",
        district="Gaborone",
        region="South-East"
    )
    clinic2 = Clinic(
        id=uuid4(),
        name="Francistown Clinic",
        district="Francistown",
        region="North-East"
    )
    db_session.add_all([clinic1, clinic2])
    db_session.commit()
    
    # Filter by Gaborone
    clinics = service.get_clinics(test_user, db_session, district="Gaborone")
    
    assert any(c.id == clinic1.id for c in clinics)
    assert not any(c.id == clinic2.id for c in clinics)

