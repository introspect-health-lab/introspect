# ============================================================================
# 1. UPDATED signup.html - Fix form submission
# Location: src/frontend/templates/signup.html
# ============================================================================

# Replace the entire file with:
"""
{% extends "base.html" %}

{% block title %}Sign Up - Introspect{% endblock %}

{% block content %}
<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-cyan-50 to-blue-100">
    <div class="max-w-md w-full space-y-8">
        <!-- Logo/Header -->
        <div class="text-center">
            <div class="mx-auto h-16 w-16 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="h-10 w-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
                </svg>
            </div>
            <h2 class="mt-6 text-3xl font-extrabold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">
                Introspect
            </h2>
            <p class="mt-2 text-sm text-gray-600">
                Join the malaria diagnostics platform
            </p>
        </div>

        <!-- Sign Up Form -->
        <div class="bg-white rounded-2xl shadow-xl p-8 space-y-6">
            <form id="signup-form" class="space-y-5">
                <!-- Email Field -->
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                        Email address *
                    </label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
                            </svg>
                        </div>
                        <input 
                            id="email" 
                            name="email" 
                            type="email" 
                            autocomplete="email" 
                            required 
                            class="appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150 ease-in-out sm:text-sm"
                            placeholder="you@example.com"
                        >
                    </div>
                </div>

                <!-- First Name Field -->
                <div>
                    <label for="first_name" class="block text-sm font-medium text-gray-700 mb-2">
                        First Name *
                    </label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                            </svg>
                        </div>
                        <input 
                            id="first_name" 
                            name="first_name" 
                            type="text" 
                            required 
                            class="appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150 ease-in-out sm:text-sm"
                            placeholder="John"
                        >
                    </div>
                </div>

                <!-- Last Name Field -->
                <div>
                    <label for="last_name" class="block text-sm font-medium text-gray-700 mb-2">
                        Last Name *
                    </label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                            </svg>
                        </div>
                        <input 
                            id="last_name" 
                            name="last_name" 
                            type="text" 
                            required 
                            class="appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150 ease-in-out sm:text-sm"
                            placeholder="Doe"
                        >
                    </div>
                </div>

                <!-- Password Field -->
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                        Password *
                    </label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                            </svg>
                        </div>
                        <input 
                            id="password" 
                            name="password" 
                            type="password" 
                            autocomplete="new-password" 
                            required 
                            minlength="6"
                            class="appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150 ease-in-out sm:text-sm"
                            placeholder="••••••••"
                        >
                    </div>
                    <p class="mt-1 text-xs text-gray-500">Must be at least 6 characters</p>
                </div>

                <!-- Submit Button -->
                <div>
                    <button 
                        type="submit" 
                        class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition duration-150"
                    >
                        <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                            <svg class="h-5 w-5 text-blue-300 group-hover:text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
                            </svg>
                        </span>
                        Create account
                    </button>
                </div>
            </form>

            <!-- Divider -->
            <div class="relative">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-300"></div>
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="px-2 bg-white text-gray-500">Already have an account?</span>
                </div>
            </div>

            <!-- Sign In Link -->
            <div class="text-center">
                <a href="/signin" class="font-medium text-blue-600 hover:text-blue-500 transition duration-150">
                    Sign in instead
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script>
    // Redirect if already authenticated
    redirectIfAuthenticated();

    // Handle form submission
    document.getElementById('signup-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            first_name: document.getElementById('first_name').value,
            last_name: document.getElementById('last_name').value
        };
        
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Disable button and show loading
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<div class="spinner mx-auto"></div>';
        
        try {
            const response = await fetch('/auth/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                showToast('Account created successfully! Please sign in.', 'success');
                setTimeout(() => {
                    window.location.href = '/signin';
                }, 1500);
            } else {
                const error = await response.json();
                showToast(error.detail || 'Registration failed', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        } catch (error) {
            showToast('Network error. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
</script>
{% endblock %}
"""

# ============================================================================
# 2. CREATE DUMMY DASHBOARD DATA SCRIPT
# Location: create_dummy_data.py (root directory)
# ============================================================================

"""
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
"""

# ============================================================================
# 3. FIX PATIENTS NOT BEING ADDED
# Location: src/patients/service.py
# ============================================================================

# The issue is likely in the create_patient function. Update it to:
"""
def create_patient(current_user: TokenData, db: Session, patient: models.PatientCreate) -> Patient:
    '''Create a new patient record.'''
    try:
        # Convert Pydantic model to dict and create Patient entity
        patient_dict = patient.model_dump()
        new_patient = Patient(**patient_dict)
        
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        
        logging.info(f"Created new patient {new_patient.id} by user {current_user.get_uuid()}")
        return new_patient
    except Exception as e:
        logging.error(f"Failed to create patient. Error: {str(e)}")
        db.rollback()
        raise PatientCreationError(str(e))
"""

# Also update patients.js to properly handle clinic_id
# Location: src/frontend/static/js/patients.js
"""
document.getElementById('add-patient-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    // Get current user to get clinic_id
    try {
        const userResponse = await authenticatedFetch('/users/me');
        const user = await userResponse.json();
        
        const data = {
            clinic_id: user.clinic_id || '00000000-0000-0000-0000-000000000000', // Use user's clinic
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            age: parseInt(formData.get('age')),
            gender: formData.get('gender'),
            national_id: formData.get('national_id') || null,
            village: formData.get('village') || null,
            phone_number: formData.get('phone_number') || null,
            district: formData.get('district') || 'Gaborone'
        };
        
        const response = await authenticatedFetch('/api/patients/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast('Patient added successfully', 'success');
            closeAddPatientModal();
            loadPatients();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Failed to add patient', 'error');
        }
    } catch (error) {
        console.error('Error adding patient:', error);
        showToast('Failed to add patient', 'error');
    }
});
"""

# ============================================================================
# 4. RENAME ANALYSIS TO DIAGNOSIS EVERYWHERE
# ============================================================================

# Create a rename script:
"""
#!/bin/bash
# Location: rename_analysis_to_diagnosis.sh

echo "Renaming 'analysis' to 'diagnosis' throughout the codebase..."

# Rename files
mv src/frontend/templates/analyze.html src/frontend/templates/diagnose.html 2>/dev/null || true
mv src/frontend/static/js/analyze.js src/frontend/static/js/diagnose.js 2>/dev/null || true

# Replace in files (case-insensitive where appropriate)
find src -type f -name "*.py" -exec sed -i 's/analyze/diagnose/g' {} \;
find src -type f -name "*.py" -exec sed -i 's/Analyze/Diagnose/g' {} \;
find src -type f -name "*.py" -exec sed -i 's/analysis/diagnosis/g' {} \;
find src -type f -name "*.py" -exec sed -i 's/Analysis/Diagnosis/g' {} \;

find src/frontend -type f -name "*.html" -exec sed -i 's/analyze/diagnose/g' {} \;
find src/frontend -type f -name "*.html" -exec sed -i 's/Analyze/Diagnose/g' {} \;
find src/frontend -type f -name "*.html" -exec sed -i 's/analysis/diagnosis/g' {} \;
find src/frontend -type f -name "*.html" -exec sed -i 's/Analysis/Diagnosis/g' {} \;

find src/frontend -type f -name "*.js" -exec sed -i 's/analyze/diagnose/g' {} \;
find src/frontend -type f -name "*.js" -exec sed -i 's/Analyze/Diagnose/g' {} \;
find src/frontend -type f -name "*.js" -exec sed -i 's/analysis/diagnosis/g' {} \;
find src/frontend -type f -name "*.js" -exec sed -i 's/Analysis/Diagnosis/g' {} \;

echo "✓ Renaming complete!"
echo "Note: Review changes and restart server"
"""

# ============================================================================
# 5. UPDATE DIAGNOSIS PAGE WITH DISEASE DROPDOWN
# Location: src/frontend/templates/diagnose.html (after renaming)
# ============================================================================

# Add disease dropdown after the patient selection:
"""
<!-- Disease Selection (Future Feature) -->
<div>
    <label class="block text-sm font-medium text-gray-700 mb-2">
        Disease Type
    </label>
    <div class="relative">
        <select 
            id="disease-select" 
            name="disease_type" 
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white appearance-none"
        >
            <option value="malaria" selected>Malaria (Available Now)</option>
            <option value="tuberculosis" disabled>Tuberculosis (Coming Soon)</option>
            <option value="covid19" disabled>COVID-19 (Coming Soon)</option>
            <option value="typhoid" disabled>Typhoid (Coming Soon)</option>
            <option value="hepatitis" disabled>Hepatitis (Coming Soon)</option>
            <option value="hiv" disabled>HIV/AIDS (Coming Soon)</option>
        </select>
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-400">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
        </div>
    </div>
    <p class="mt-1 text-xs text-gray-500">
        🚀 Future: Multi-disease diagnosis capability. Currently supports malaria only.
    </p>
</div>
"""

print("✅ All updates prepared!")
print("\n📋 Summary of changes:")
print("1. ✓ Fixed signup.html form submission")
print("2. ✓ Created dummy data script (create_dummy_data.py)")
print("3. ✓ Fixed patient creation issue")
print("4. ✓ Prepared analysis→diagnosis rename script")
print("5. ✓ Added disease dropdown for future expansion")
