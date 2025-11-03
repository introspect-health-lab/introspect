import pytest
from uuid import uuid4
from datetime import date
from sqlalchemy.orm import Session
from src.patients import service, models
from src.entities.patient import Patient, Gender
from src.entities.clinic import Clinic
from src.auth.models import TokenData
from src.exceptions import PatientNotFoundError

@pytest.fixture
def test_clinic(db_session: Session):
    """Create a test clinic."""
    clinic = Clinic(
        id=uuid4(),
        name="Test Clinic",
        district="Gaborone",
        region="South-East"
    )
    db_session.add(clinic)
    db_session.commit()
    db_session.refresh(clinic)
    return clinic

@pytest.fixture
def test_user():
    """Create a test user token."""
    return TokenData(user_id=str(uuid4()))

@pytest.fixture
def test_patient(db_session: Session, test_clinic: Clinic):
    """Create a test patient."""
    patient = Patient(
        id=uuid4(),
        clinic_id=test_clinic.id,
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        age=33,
        gender=Gender.Male,
        national_id="123456789"
    )
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    return patient

def test_create_patient(db_session: Session, test_user: TokenData, test_clinic: Clinic):
    """Test creating a new patient."""
    patient_data = models.PatientCreate(
        clinic_id=test_clinic.id,
        first_name="Jane",
        last_name="Smith",
        date_of_birth=date(1995, 5, 15),
        age=28,
        gender=Gender.Female,
        phone_number="+267 71234567",
        national_id="987654321",
        village="Mogoditshane",
        district="Gaborone"
    )
    
    patient = service.create_patient(test_user, db_session, patient_data)
    
    assert patient.id is not None
    assert patient.first_name == "Jane"
    assert patient.last_name == "Smith"
    assert patient.gender == Gender.Female
    assert patient.clinic_id == test_clinic.id

def test_get_patients(db_session: Session, test_user: TokenData, test_patient: Patient):
    """Test retrieving all patients."""
    patients = service.get_patients(test_user, db_session)
    
    assert len(patients) >= 1
    assert any(p.id == test_patient.id for p in patients)

def test_get_patient_by_id(db_session: Session, test_user: TokenData, test_patient: Patient):
    """Test retrieving a patient by ID."""
    patient = service.get_patient_by_id(test_user, db_session, test_patient.id)
    
    assert patient.id == test_patient.id
    assert patient.first_name == test_patient.first_name
    assert patient.last_name == test_patient.last_name

def test_get_patient_by_id_not_found(db_session: Session, test_user: TokenData):
    """Test retrieving a non-existent patient."""
    with pytest.raises(PatientNotFoundError):
        service.get_patient_by_id(test_user, db_session, uuid4())

def test_search_patients(db_session: Session, test_user: TokenData, test_patient: Patient):
    """Test searching patients by name."""
    patients = service.search_patients(test_user, db_session, "John")
    
    assert len(patients) >= 1
    assert any(p.id == test_patient.id for p in patients)

def test_search_patients_by_national_id(db_session: Session, test_user: TokenData, test_patient: Patient):
    """Test searching patients by national ID."""
    patients = service.search_patients(test_user, db_session, "123456789")
    
    assert len(patients) >= 1
    assert any(p.id == test_patient.id for p in patients)

def test_update_patient(db_session: Session, test_user: TokenData, test_patient: Patient):
    """Test updating a patient."""
    update_data = models.PatientUpdate(
        phone_number="+267 72345678",
        village="Tlokweng"
    )
    
    updated_patient = service.update_patient(test_user, db_session, test_patient.id, update_data)
    
    assert updated_patient.phone_number == "+267 72345678"
    assert updated_patient.village == "Tlokweng"
    assert updated_patient.first_name == test_patient.first_name  # Unchanged

def test_delete_patient(db_session: Session, test_user: TokenData, test_patient: Patient):
    """Test deleting a patient."""
    patient_id = test_patient.id
    
    service.delete_patient(test_user, db_session, patient_id)
    
    with pytest.raises(PatientNotFoundError):
        service.get_patient_by_id(test_user, db_session, patient_id)

def test_get_patients_filtered_by_clinic(db_session: Session, test_user: TokenData, test_clinic: Clinic):
    """Test filtering patients by clinic."""
    # Create patients in different clinics
    other_clinic = Clinic(
        id=uuid4(),
        name="Other Clinic",
        district="Francistown",
        region="North-East"
    )
    db_session.add(other_clinic)
    db_session.commit()
    
    patient1 = Patient(
        id=uuid4(),
        clinic_id=test_clinic.id,
        first_name="Patient",
        last_name="One",
        gender=Gender.Male,
        age=25
    )
    patient2 = Patient(
        id=uuid4(),
        clinic_id=other_clinic.id,
        first_name="Patient",
        last_name="Two",
        gender=Gender.Female,
        age=30
    )
    db_session.add_all([patient1, patient2])
    db_session.commit()
    
    # Filter by test_clinic
    patients = service.get_patients(test_user, db_session, clinic_id=test_clinic.id)
    
    assert any(p.id == patient1.id for p in patients)
    assert not any(p.id == patient2.id for p in patients)

