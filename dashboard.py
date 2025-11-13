#!/usr/bin/env python3
'''
Create dummy data for Introspect dashboard
Run this script to populate the database with sample data
'''

import sys
from datetime import datetime, timedelta
from uuid import uuid4
import random

# Add project root to path
sys.path.insert(0, '.')

from src.database.core import SessionLocal
from src.entities.user import User, UserRole
from src.entities.clinic import Clinic
from src.entities.patient import Patient, Gender
from src.entities.test_result import TestResult, TestStatus, SyncStatus
from src.auth.service import get_password_hash

def create_dummy_data():
    '''Create comprehensive dummy data for dashboard'''
    db = SessionLocal()
    
    try:
        print("🔬 Creating dummy data for Introspect Dashboard...")
        print("=" * 60)
        
        # 1. Create Admin User
        print("\n📋 Creating admin user...")
        admin = User(
            id=uuid4(),
            email="admin@introspect.com",
            first_name="Admin",
            last_name="User",
            password_hash=get_password_hash("Admin123!"),
            role=UserRole.Admin,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print(f"✓ Admin created: admin@introspect.com / Admin123!")
        
        # 2. Create Clinics
        print("\n🏥 Creating clinics...")
        clinics_data = [
            {"name": "Princess Marina Hospital", "district": "Gaborone", "region": "South-East", "lat": -24.6541, "lon": 25.9087},
            {"name": "Nyangabgwe Hospital", "district": "Francistown", "region": "North-East", "lat": -21.1699, "lon": 27.5084},
            {"name": "Scottish Livingstone Hospital", "district": "Molepolole", "region": "Kweneng", "lat": -24.4085, "lon": 25.4950},
            {"name": "Sekgoma Memorial Hospital", "district": "Serowe", "region": "Central", "lat": -22.3925, "lon": 26.7102},
            {"name": "Maun General Hospital", "district": "Maun", "region": "North-West", "lat": -19.9833, "lon": 23.4167},
            {"name": "Lobatse Mental Hospital", "district": "Lobatse", "region": "South-East", "lat": -25.2243, "lon": 25.6846},
        ]
        
        clinics = []
        for i, clinic_data in enumerate(clinics_data):
            clinic = Clinic(
                id=uuid4(),
                name=clinic_data["name"],
                district=clinic_data["district"],
                region=clinic_data["region"],
                latitude=clinic_data["lat"],
                longitude=clinic_data["lon"],
                contact_phone=f"+267 {random.randint(300, 399)}{random.randint(1000, 9999)}",
                contact_email=f"info@{clinic_data['name'].lower().replace(' ', '')}.bw"
            )
            clinics.append(clinic)
            db.add(clinic)
            print(f"  ✓ {clinic.name} ({clinic.district})")
        
        db.commit()
        
        # 3. Create Health Workers
        print("\n👨‍⚕️ Creating health workers...")
        health_workers = []
        worker_names = [
            ("Dr. Thabo", "Molefe"), ("Nurse Kefilwe", "Kgosana"), 
            ("Dr. Mpho", "Moeti"), ("Nurse Lesego", "Seretse"),
            ("Lab Tech Kgosi", "Mogapi"), ("Dr. Boitumelo", "Tsheko")
        ]
        
        for i, (first, last) in enumerate(worker_names):
            clinic = clinics[i % len(clinics)]
            worker = User(
                id=uuid4(),
                email=f"{first.lower().replace('.', '').replace(' ', '')}.{last.lower()}@health.bw",
                first_name=first.replace('Dr. ', '').replace('Nurse ', '').replace('Lab Tech ', ''),
                last_name=last,
                password_hash=get_password_hash("Worker123!"),
                role=UserRole.HealthWorker,
                clinic_id=clinic.id,
                is_active=True
            )
            health_workers.append(worker)
            db.add(worker)
            print(f"  ✓ {first} {last} at {clinic.name}")
        
        db.commit()
        
        # 4. Create Patients
        print("\n👥 Creating patients...")
        first_names = ["Thabo", "Kefilwe", "Mpho", "Lesego", "Kgosi", "Boitumelo", "Tshepo", "Neo", 
                      "Kagiso", "Ontlametse", "Tebogo", "Lorato", "Kitso", "Mpule", "Gofaone"]
        last_names = ["Molefe", "Kgosana", "Moeti", "Seretse", "Mogapi", "Tsheko", "Gabaake", "Modise",
                     "Mothibi", "Tau", "Montsho", "Khunou", "Segwai", "Marope", "Sebudubudu"]
        villages = ["Mogoditshane", "Tlokweng", "Gaborone West", "Block 8", "Phakalane", 
                   "Broadhurst", "Mmopane", "Gabane", "Molepolole", "Mochudi"]
        
        patients = []
        for i in range(100):  # Create 100 patients
            clinic = random.choice(clinics)
            birth_year = random.randint(1950, 2020)
            patient = Patient(
                id=uuid4(),
                clinic_id=clinic.id,
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                date_of_birth=datetime(birth_year, random.randint(1, 12), random.randint(1, 28)),
                age=2024 - birth_year,
                gender=random.choice([Gender.Male, Gender.Female]),
                phone_number=f"+267 {random.randint(70000000, 79999999)}",
                national_id=f"{random.randint(100000000, 999999999)}",
                village=random.choice(villages),
                district=clinic.district
            )
            patients.append(patient)
            db.add(patient)
        
        print(f"  ✓ Created {len(patients)} patients")
        db.commit()
        
        # 5. Create Test Results (Last 90 days)
        print("\n🔬 Creating test results...")
        base_date = datetime.now()
        test_count = 0
        
        for days_ago in range(90):  # Last 90 days
            test_date = base_date - timedelta(days=days_ago)
            
            # Vary number of tests per day (more recent = more tests)
            tests_per_day = random.randint(3, 15) if days_ago < 30 else random.randint(1, 5)
            
            for _ in range(tests_per_day):
                patient = random.choice(patients)
                worker = random.choice([w for w in health_workers if w.clinic_id == patient.clinic_id] or health_workers)
                
                # Simulate realistic positivity rate (5-15%)
                is_positive = random.random() < 0.10  # 10% positive rate
                
                if is_positive:
                    result_status = TestStatus.Positive
                    confidence = random.uniform(0.75, 0.98)
                else:
                    result_status = TestStatus.Negative
                    confidence = random.uniform(0.80, 0.99)
                
                # Small chance of inconclusive
                if random.random() < 0.05:
                    result_status = TestStatus.Inconclusive
                    confidence = random.uniform(0.50, 0.70)
                
                test_result = TestResult(
                    id=uuid4(),
                    patient_id=patient.id,
                    clinic_id=patient.clinic_id,
                    health_worker_id=worker.id,
                    test_date=test_date,
                    result=result_status,
                    confidence_score=confidence,
                    image_path=f"uploads/{patient.clinic_id}/{test_date.strftime('%Y-%m')}/{uuid4()}.jpg",
                    image_filename=f"blood_smear_{uuid4()}.jpg",
                    model_version="v1.0.0-dummy",
                    processing_time_ms=random.uniform(200, 800),
                    sync_status=SyncStatus.Synced if random.random() > 0.1 else SyncStatus.Pending,
                    synced_at=test_date if random.random() > 0.1 else None
                )
                db.add(test_result)
                test_count += 1
        
        print(f"  ✓ Created {test_count} test results over 90 days")
        db.commit()
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ Dummy data creation complete!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"  Users:        1 admin + {len(health_workers)} health workers")
        print(f"  Clinics:      {len(clinics)}")
        print(f"  Patients:     {len(patients)}")
        print(f"  Test Results: {test_count}")
        print(f"\n🔐 Login Credentials:")
        print(f"  Admin:  admin@introspect.com / Admin123!")
        print(f"  Worker: {health_workers[0].email} / Worker123!")
        print(f"\n🌐 Access:")
        print(f"  Web UI:   http://localhost:8000")
        print(f"  API Docs: http://localhost:8000/api/docs")
        print(f"  Dashboard: http://localhost:8000/dashboard")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error creating dummy data: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_dummy_data()