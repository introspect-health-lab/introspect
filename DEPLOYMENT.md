# Introspect Deployment Guide

This guide covers deploying the Introspect malaria diagnostics system to production.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [Security Considerations](#security-considerations)
8. [Monitoring & Logging](#monitoring--logging)

---

## Prerequisites

### Required Software
- Python 3.11+
- PostgreSQL 15+ (production)
- Docker & Docker Compose (optional)
- Git

### Required Services
- PostgreSQL database
- File storage (local or S3)
- (Optional) Central sync server

---

## Local Development

### 1. Clone Repository
```bash
git clone <repository-url>
cd introspect
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For testing
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run Database Migrations
```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Seed Database (Optional)
```bash
python seed_data.py
```

### 7. Start Development Server
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at: http://localhost:8000/docs

---

## Docker Deployment

### Development with Docker

```bash
# Build and start all services
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f api

# Stop services
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v
```

### Production Docker Setup

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: introspect
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
    networks:
      - introspect-network

  api:
    build: .
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/introspect
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: production
    volumes:
      - ./uploads:/app/uploads
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: always
    networks:
      - introspect-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: always
    networks:
      - introspect-network

volumes:
  postgres_data:

networks:
  introspect-network:
    driver: bridge
```

---

## Production Deployment

### Option 1: Traditional Server (Ubuntu/Debian)

#### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Dependencies
```bash
# Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Nginx
sudo apt install nginx -y

# Supervisor (process manager)
sudo apt install supervisor -y
```

#### 3. Create Application User
```bash
sudo useradd -m -s /bin/bash introspect
sudo su - introspect
```

#### 4. Deploy Application
```bash
cd /home/introspect
git clone <repository-url> app
cd app
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. Configure PostgreSQL
```bash
sudo -u postgres psql

CREATE DATABASE introspect;
CREATE USER introspect_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE introspect TO introspect_user;
\q
```

#### 6. Configure Environment
```bash
nano /home/introspect/app/.env
```

Add:
```env
DATABASE_URL=postgresql://introspect_user:secure_password@localhost/introspect
SECRET_KEY=<generate-secure-key>
ENVIRONMENT=production
```

#### 7. Run Migrations
```bash
cd /home/introspect/app
source venv/bin/activate
alembic upgrade head
```

#### 8. Configure Supervisor
```bash
sudo nano /etc/supervisor/conf.d/introspect.conf
```

Add:
```ini
[program:introspect]
directory=/home/introspect/app
command=/home/introspect/app/venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 4
user=introspect
autostart=true
autorestart=true
stderr_logfile=/var/log/introspect/err.log
stdout_logfile=/var/log/introspect/out.log
```

```bash
sudo mkdir -p /var/log/introspect
sudo chown introspect:introspect /var/log/introspect
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start introspect
```

#### 9. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/introspect
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads {
        alias /home/introspect/app/uploads;
        internal;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/introspect /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 10. Setup SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Option 2: Cloud Deployment (AWS, GCP, Azure)

#### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 introspect

# Create environment
eb create introspect-prod

# Deploy
eb deploy
```

#### Google Cloud Run
```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/introspect

# Deploy
gcloud run deploy introspect \
  --image gcr.io/PROJECT_ID/introspect \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure App Service
```bash
# Create resource group
az group create --name introspect-rg --location eastus

# Create app service plan
az appservice plan create --name introspect-plan --resource-group introspect-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group introspect-rg --plan introspect-plan --name introspect --runtime "PYTHON|3.11"

# Deploy
az webapp up --name introspect
```

---

## Environment Variables

### Required Variables
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/introspect

# Security
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=production
DEBUG=false
```

### Optional Variables
```env
# AI Model
AI_MODEL_PATH=/path/to/model.tflite

# File Storage
UPLOAD_DIR=/app/uploads
MAX_UPLOAD_SIZE=20971520  # 20MB

# Sync Service
SYNC_SERVER_URL=https://central.introspect.example.com
SYNC_API_KEY=<api-key>

# CORS
ALLOWED_ORIGINS=https://app.introspect.com,https://admin.introspect.com

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=<sentry-dsn>
```

---

## Database Setup

### PostgreSQL Production Configuration

```sql
-- Create database
CREATE DATABASE introspect;

-- Create user
CREATE USER introspect_user WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE introspect TO introspect_user;

-- Connect to database
\c introspect

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO introspect_user;
```

### Backup Strategy

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/introspect"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump -U introspect_user introspect > $BACKUP_DIR/introspect_$DATE.sql
gzip $BACKUP_DIR/introspect_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

---

## Security Considerations

### 1. Secrets Management
- Use environment variables for secrets
- Never commit secrets to Git
- Use AWS Secrets Manager, Azure Key Vault, or similar

### 2. Database Security
- Use strong passwords
- Enable SSL connections
- Restrict network access
- Regular backups

### 3. API Security
- Enable HTTPS only
- Implement rate limiting
- Use strong JWT secrets
- Regular security updates

### 4. File Upload Security
- Validate file types
- Scan for malware
- Limit file sizes
- Store outside web root

---

## Monitoring & Logging

### Application Monitoring

```python
# Add to src/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    environment=os.getenv("ENVIRONMENT", "production")
)
```

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

### Log Aggregation

Use services like:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Datadog
- CloudWatch (AWS)
- Stackdriver (GCP)

---

## Maintenance

### Regular Tasks
- [ ] Daily database backups
- [ ] Weekly security updates
- [ ] Monthly dependency updates
- [ ] Quarterly security audits

### Monitoring Checklist
- [ ] API response times
- [ ] Error rates
- [ ] Database performance
- [ ] Disk space
- [ ] Memory usage
- [ ] CPU usage

---

## Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U introspect_user -d introspect -h localhost
```

**Application Won't Start**
```bash
# Check logs
sudo supervisorctl tail -f introspect stderr

# Check environment
cat /home/introspect/app/.env
```

**High Memory Usage**
```bash
# Reduce workers
# In supervisor config: --workers 2
```

---

## Support

For deployment issues:
- Check logs: `/var/log/introspect/`
- Review documentation
- Open GitHub issue
- Contact DevOps team

