"""
Seed script to populate the Introspect database with sample data.
Run this after starting the server to create demo clinics, patients, and test results.

Usage:
    python seed_data.py
"""

import requests
import sys
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8000"

def create_user_and_login():
    """Create a demo user and get authentication token."""
    print("Creating demo user...")
    
    # Register user
    response = requests.post(f"{BASE_URL}/auth/", json={
        "email": "demo@introspect.com",
        "password": "Demo123!",
        "first_name": "Demo",
        "last_name": "User"
    })
    
    if response.status_code == 201:
        print("✓ Demo user created")
    elif response.status_code == 400:
        print("✓ Demo user already exists")
    else:
        print(f"✗ Failed to create user: {response.text}")
        return None
    
    # Login
    print("Logging in...")
    response = requests.post(f"{BASE_URL}/auth/token", data={
        "username": "demo@introspect.com",
        "password": "Demo123!"
    })
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✓ Logged in successfully")
        return token
    else:
        print(f"✗ Failed to login: {response.text}")
        return None

def create_clinics(headers):
    """Create sample clinics."""
    print("\nCreating clinics...")
    
    clinics_data = [
        {
            "name": "Central Health Clinic",
            "district": "Gaborone",
            "region": "South-East",
            "latitude": -24.6282,
            "longitude": 25.9231,
            "contact_phone": "+267 3900000",
            "contact_email": "central@health.bw"
        },
        {
            "name": "Princess Marina Hospital",
            "district": "Gaborone",
            "region": "South-East",
            "latitude": -24.6541,
            "longitude": 25.9087,
            "contact_phone": "+267 3953221",
            "contact_email": "pmh@health.bw"
        },
        {
            "name": "Nyangabgwe Referral Hospital",
            "district": "Francistown",
            "region": "North-East",
            "latitude": -21.1699,
            "longitude": 27.5084,
            "contact_phone": "+267 2412000",
            "contact_email": "nyangabgwe@health.bw"
        },
        {
            "name": "Maun General Hospital",
            "district": "Maun",
            "region": "North-West",
            "latitude": -19.9833,
            "longitude": 23.4167,
            "contact_phone": "+267 6860444",
            "contact_email": "maun@health.bw"
        }
    ]
    
    clinic_ids = []
    for clinic_data in clinics_data:
        response = requests.post(f"{BASE_URL}/api/clinics", headers=headers, json=clinic_data)
        if response.status_code == 201:
            clinic_id = response.json()["id"]
            clinic_ids.append(clinic_id)
            print(f"✓ Created clinic: {clinic_data['name']}")
        else:
            print(f"✗ Failed to create clinic {clinic_data['name']}: {response.text}")
    
    return clinic_ids

def create_patients(headers, clinic_ids):
    """Create sample patients."""
    print("\nCreating patients...")
    
    first_names = ["Thabo", "Kefilwe", "Mpho", "Lesego", "Kgosi", "Boitumelo", "Tshepo", "Neo"]
    last_names = ["Molefe", "Kgosana", "Moeti", "Seretse", "Mogapi", "Tsheko", "Gabaake", "Modise"]
    villages = ["Mogoditshane", "Tlokweng", "Gaborone West", "Block 8", "Phakalane", "Broadhurst"]
    
    patient_ids = []
    for i in range(20):
        clinic_id = random.choice(clinic_ids)
        patient_data = {
            "clinic_id": clinic_id,
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "age": random.randint(5, 75),
            "gender": random.choice(["male", "female"]),
            "phone_number": f"+267 7{random.randint(1000000, 9999999)}",
            "national_id": f"{random.randint(100000000, 999999999)}",
            "village": random.choice(villages),
            "district": "Gaborone"
        }
        
        response = requests.post(f"{BASE_URL}/api/patients", headers=headers, json=patient_data)
        if response.status_code == 201:
            patient_id = response.json()["id"]
            patient_ids.append((patient_id, clinic_id))
            print(f"✓ Created patient: {patient_data['first_name']} {patient_data['last_name']}")
        else:
            print(f"✗ Failed to create patient: {response.text}")
    
    return patient_ids

def create_test_results(headers, patient_ids):
    """Create sample test results (without actual images)."""
    print("\nNote: Test results require image upload via multipart/form-data.")
    print("To create test results, use the /api/results/analyze endpoint with actual images.")
    print("You can use the Swagger UI at http://localhost:8000/docs to upload test images.")
    
    # We can't easily create test results via this script because they require file uploads
    # Users should use the Swagger UI or create a separate script with file handling
    
    return []

def main():
    """Main function to seed the database."""
    print("=" * 60)
    print("Introspect Database Seeding Script")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code != 200:
            print("✗ Server is not responding. Please start the server first:")
            print("  uvicorn src.main:app --reload")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Please start the server first:")
        print("  uvicorn src.main:app --reload")
        sys.exit(1)
    
    # Create user and login
    token = create_user_and_login()
    if not token:
        print("\n✗ Failed to authenticate. Exiting.")
        sys.exit(1)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create sample data
    clinic_ids = create_clinics(headers)
    if not clinic_ids:
        print("\n✗ No clinics created. Exiting.")
        sys.exit(1)
    
    patient_ids = create_patients(headers, clinic_ids)
    if not patient_ids:
        print("\n✗ No patients created. Exiting.")
        sys.exit(1)
    
    create_test_results(headers, patient_ids)
    
    # Summary
    print("\n" + "=" * 60)
    print("Seeding Complete!")
    print("=" * 60)
    print(f"✓ Created {len(clinic_ids)} clinics")
    print(f"✓ Created {len(patient_ids)} patients")
    print("\nNext steps:")
    print("1. Visit http://localhost:8000/docs to explore the API")
    print("2. Use the /api/results/analyze endpoint to upload blood smear images")
    print("3. Check the dashboard at /api/dashboard")
    print("\nDemo credentials:")
    print("  Email: demo@introspect.com")
    print("  Password: Demo123!")
    print("=" * 60)

if __name__ == "__main__":
    main()

