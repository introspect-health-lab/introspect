#!/usr/bin/env python3
"""
Introspect System Diagnostics Script
Run this to debug and profile your system
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} (Need 3.11+)")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("Checking Dependencies")
    
    required = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'alembic', 'psycopg2',
        'slowapi', 'pyjwt', 'passlib', 'pydantic', 'pillow', 'numpy'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print_warning(f"\nInstall missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    return True

def check_project_structure():
    """Verify project structure"""
    print_header("Checking Project Structure")
    
    required_dirs = [
        'src', 'src/entities', 'src/infrastructure', 'src/application',
        'src/presentation', 'src/patients', 'src/results', 'src/dashboard',
        'src/clinics', 'src/sync', 'tests', 'logs', 'uploads', 'models'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print_success(f"{dir_path}/")
        else:
            print_error(f"{dir_path}/ - MISSING")
            all_exist = False
    
    return all_exist

def check_imports():
    """Check if all modules can be imported"""
    print_header("Checking Module Imports")
    
    modules = [
        'src.main',
        'src.entities.user',
        'src.entities.clinic',
        'src.entities.patient',
        'src.entities.test_result',
        'src.infrastructure.ai_inference',
        'src.infrastructure.file_storage',
        'src.infrastructure.sync_service',
        'src.database.core',
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print_success(f"{module}")
        except Exception as e:
            print_error(f"{module} - {str(e)}")
            all_ok = False
    
    return all_ok

def check_database():
    """Check database connection"""
    print_header("Checking Database")
    
    try:
        from src.database.core import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print_success("Database connection successful")
            
            # Check tables
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            required_tables = ['users', 'clinics', 'patients', 'test_results']
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                print_warning(f"Missing tables: {', '.join(missing_tables)}")
                print_warning("Run: alembic upgrade head")
                return False
            else:
                print_success(f"All required tables exist ({len(tables)} total)")
            
            return True
    except Exception as e:
        print_error(f"Database error: {str(e)}")
        return False

def check_env_config():
    """Check environment configuration"""
    print_header("Checking Environment Configuration")
    
    from src.config import settings
    
    checks = [
        ("DATABASE_URL", settings.DATABASE_URL, settings.DATABASE_URL != ""),
        ("SECRET_KEY", settings.SECRET_KEY, 
         settings.SECRET_KEY != "your-secret-key-change-in-production"),
        ("UPLOAD_DIR", settings.UPLOAD_DIR, Path(settings.UPLOAD_DIR).exists()),
        ("LOG_FILE", settings.LOG_FILE, Path(settings.LOG_FILE).parent.exists()),
    ]
    
    all_ok = True
    for name, value, is_ok in checks:
        if is_ok:
            print_success(f"{name}: {value if len(str(value)) < 50 else '***'}")
        else:
            print_error(f"{name}: NOT CONFIGURED")
            all_ok = False
    
    if settings.SECRET_KEY == "your-secret-key-change-in-production":
        print_warning("SECRET_KEY is using default value - CHANGE IN PRODUCTION!")
    
    return all_ok

def run_tests():
    """Run test suite"""
    print_header("Running Tests")
    
    try:
        import pytest
        result = pytest.main(['-v', '--tb=short', 'tests/'])
        if result == 0:
            print_success("All tests passed")
            return True
        else:
            print_error("Some tests failed")
            return False
    except Exception as e:
        print_error(f"Test error: {str(e)}")
        return False

def profile_performance():
    """Profile API performance"""
    print_header("Profiling Performance")
    
    try:
        from fastapi.testclient import TestClient
        from src.main import app
        import time
        
        client = TestClient(app)
        
        endpoints = [
            ("GET", "/health"),
            ("GET", "/"),
        ]
        
        for method, endpoint in endpoints:
            start = time.time()
            response = getattr(client, method.lower())(endpoint)
            elapsed = (time.time() - start) * 1000
            
            if response.status_code < 400 and elapsed < 200:
                print_success(f"{method} {endpoint}: {elapsed:.2f}ms")
            elif response.status_code < 400:
                print_warning(f"{method} {endpoint}: {elapsed:.2f}ms (SLOW)")
            else:
                print_error(f"{method} {endpoint}: {response.status_code}")
        
        return True
    except Exception as e:
        print_error(f"Profiling error: {str(e)}")
        return False

def check_storage():
    """Check file storage"""
    print_header("Checking File Storage")
    
    try:
        from src.infrastructure.file_storage import get_storage_service
        
        storage = get_storage_service()
        stats = storage.get_storage_stats()
        
        print_success(f"Storage initialized at: {stats['base_path']}")
        print_success(f"Total files: {stats['total_files']}")
        print_success(f"Total size: {stats['total_size_mb']} MB")
        
        return True
    except Exception as e:
        print_error(f"Storage error: {str(e)}")
        return False

def check_ai_model():
    """Check AI model"""
    print_header("Checking AI Model")
    
    try:
        from src.infrastructure.ai_inference import get_inference_service
        
        inference = get_inference_service()
        
        if inference.is_loaded:
            print_success(f"Model loaded: {inference.model_version}")
        else:
            print_warning("Model not loaded (using placeholder)")
        
        return True
    except Exception as e:
        print_error(f"AI model error: {str(e)}")
        return False

def generate_report():
    """Generate diagnostic report"""
    print_header("Generating Diagnostic Report")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "checks": {}
    }
    
    checks = [
        ("python_version", check_python_version),
        ("dependencies", check_dependencies),
        ("project_structure", check_project_structure),
        ("imports", check_imports),
        ("database", check_database),
        ("env_config", check_env_config),
        ("storage", check_storage),
        ("ai_model", check_ai_model),
        ("performance", profile_performance),
    ]
    
    for name, check_func in checks:
        try:
            result = check_func()
            report["checks"][name] = "PASS" if result else "FAIL"
        except Exception as e:
            report["checks"][name] = f"ERROR: {str(e)}"
    
    # Save report
    report_path = Path("logs") / f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print_success(f"Report saved to: {report_path}")
    
    # Summary
    print_header("Summary")
    passed = sum(1 for v in report["checks"].values() if v == "PASS")
    total = len(report["checks"])
    
    if passed == total:
        print_success(f"All checks passed ({passed}/{total})")
    else:
        print_warning(f"{passed}/{total} checks passed")
    
    return report

def main():
    """Main diagnostic function"""
    print(f"\n{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════╗")
    print("║      Introspect System Diagnostics Tool           ║")
    print("║      AI-Powered Malaria Diagnostic System         ║")
    print("╚════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    report = generate_report()
    
    # Exit code based on results
    all_passed = all(v == "PASS" for v in report["checks"].values())
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
