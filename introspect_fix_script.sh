#!/bin/bash

# Introspect - Automated Fix Script
# Fixes common issues in the system

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════╗"
echo "║      Introspect Automated Fix Script              ║"
echo "║      Fixing Common Issues...                       ║"
echo "╚════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print status
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# 1. Create missing directories
print_status "Creating missing directories..."
mkdir -p logs uploads storage/uploads models tests/unit tests/integration
print_success "Directories created"

# 2. Create .gitkeep files
print_status "Creating .gitkeep files..."
touch logs/.gitkeep uploads/.gitkeep storage/uploads/.gitkeep models/.gitkeep
print_success ".gitkeep files created"

# 3. Fix file permissions
print_status "Fixing file permissions..."
chmod -R 755 logs uploads storage models
print_success "Permissions fixed"

# 4. Check and install dependencies
print_status "Checking Python dependencies..."
if command -v pip &> /dev/null; then
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt --quiet
        print_success "Dependencies installed"
    else
        print_error "requirements.txt not found"
    fi
else
    print_error "pip not found. Please install Python pip"
fi

# 5. Setup environment file
print_status "Setting up environment file..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env created from .env.example"
        print_warning "Please update .env with your configuration"
    else
        # Create basic .env
        cat > .env << EOF
DATABASE_URL=sqlite:///./introspect.db
SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "CHANGE_ME_IN_PRODUCTION")
ENVIRONMENT=development
DEBUG=true
EOF
        print_success ".env created with defaults"
        print_warning "Please review and update .env"
    fi
else
    print_success ".env already exists"
fi

# 6. Initialize database
print_status "Initializing database..."
if [ -f "src/main.py" ]; then
    # Check if alembic is initialized
    if [ ! -d "alembic/versions" ]; then
        print_status "Initializing Alembic..."
        alembic init alembic 2>/dev/null || print_warning "Alembic already initialized"
    fi
    
    # Run migrations
    python -c "from src.database.core import Base, engine; Base.metadata.create_all(bind=engine)" 2>/dev/null && \
        print_success "Database tables created" || \
        print_warning "Database initialization issue - check logs"
else
    print_error "src/main.py not found"
fi

# 7. Fix common import issues
print_status "Fixing import paths..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "export PYTHONPATH=\"\${PYTHONPATH}:$(pwd)\"" >> ~/.bashrc 2>/dev/null || true
print_success "PYTHONPATH updated"

# 8. Clean up cache files
print_status "Cleaning up cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
rm -rf .pytest_cache htmlcov .coverage 2>/dev/null || true
print_success "Cache cleaned"

# 9. Fix Docker setup
if command -v docker &> /dev/null; then
    print_status "Checking Docker setup..."
    if [ -f "docker-compose.yml" ]; then
        docker-compose config > /dev/null 2>&1 && \
            print_success "Docker Compose configuration valid" || \
            print_warning "Docker Compose configuration has issues"
    fi
fi

# 10. Test imports
print_status "Testing Python imports..."
python -c "
try:
    from src.main import app
    print('${GREEN}[✓]${NC} All imports successful')
except ImportError as e:
    print('${RED}[✗]${NC} Import error:', str(e))
    exit(1)
" || print_error "Import test failed"

# 11. Create test configuration
print_status "Setting up test configuration..."
if [ ! -f "pytest.ini" ]; then
    cat > pytest.ini << 'EOF'
[pytest]
asyncio_mode = auto
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
testpaths = tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::UserWarning
EOF
    print_success "pytest.ini created"
fi

# 12. Setup logging
print_status "Configuring logging..."
mkdir -p logs
if [ ! -f "logs/introspect.log" ]; then
    touch logs/introspect.log
    chmod 644 logs/introspect.log
fi
print_success "Logging configured"

# 13. Fix database connection issues
print_status "Fixing database connection..."
if [ -f "introspect.db" ]; then
    # Check if database is locked
    if lsof introspect.db 2>/dev/null; then
        print_warning "Database is in use by another process"
    else
        print_success "Database is accessible"
    fi
fi

# 14. Create placeholder AI model
print_status "Setting up AI model placeholder..."
if [ ! -f "models/README.md" ]; then
    cat > models/README.md << 'EOF'
# AI Models Directory

Place your TensorFlow Lite malaria detection model here.

Expected file: `malaria_detector.tflite`

The system will use a placeholder if no model is found.
EOF
    print_success "Model directory configured"
fi

# 15. Validate configuration
print_status "Validating configuration..."
python -c "
from src.config import settings
print('Database URL:', settings.DATABASE_URL)
print('Environment:', settings.ENVIRONMENT)
print('Upload Directory:', settings.UPLOAD_DIR)
" 2>/dev/null && print_success "Configuration valid" || print_warning "Configuration validation failed"

# 16. Create startup script
print_status "Creating startup scripts..."
cat > start_dev.sh << 'EOF'
#!/bin/bash
echo "Starting Introspect in development mode..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
EOF
chmod +x start_dev.sh

cat > start_prod.sh << 'EOF'
#!/bin/bash
echo "Starting Introspect in production mode..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
EOF
chmod +x start_prod.sh

print_success "Startup scripts created"

# 17. Run diagnostic
print_status "Running system diagnostics..."
if [ -f "debug_system.py" ]; then
    python debug_system.py --no-tests || print_warning "Some diagnostics failed"
else
    print_warning "debug_system.py not found - skipping diagnostics"
fi

# Summary
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Common issues fixed!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review and update .env file"
echo "  2. Run: ./start_dev.sh (for development)"
echo "  3. Or: docker-compose up (for Docker)"
echo "  4. Access API: http://localhost:8000/docs"
echo ""
echo "For production deployment:"
echo "  1. Update SECRET_KEY in .env"
echo "  2. Configure DATABASE_URL for PostgreSQL"
echo "  3. Run: ./start_prod.sh"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
