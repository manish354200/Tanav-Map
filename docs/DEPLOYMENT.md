# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- Git
- AWS/NIC Cloud credentials (for cloud deployment)
- PostgreSQL 12+ (for production)
- Node.js 16+ and Python 3.9+ (for manual deployment)

## Quick Start with Docker

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mental-health-monitoring
```

### 2. Configure Environment
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Update environment variables as needed.

### 3. Run with Docker Compose
```bash
# Build and start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 4. Initialize Database
```bash
docker-compose exec postgres psql -U postgres -d mental_health -f /docker-entrypoint-initdb.d/01-schema.sql
```

### 5. Access Application
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- API: http://localhost:8000

## Manual Deployment

### Backend Setup

1. **Install Python Dependencies**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Setup Database**
```bash
psql -U postgres
CREATE DATABASE mental_health;
\q
psql -U postgres -d mental_health < ../database/schema.sql
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with actual values
```

4. **Run Backend**
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Configure Environment**
```bash
cp .env.example .env
# Set REACT_APP_API_URL=http://localhost:8000/api/v1
```

3. **Run Frontend**
```bash
npm start
```

## Cloud Deployment

### AWS Deployment

#### Using Elastic Beanstalk

1. **Install AWS CLI**
```bash
pip install awscli
aws configure
```

2. **Initialize Elastic Beanstalk**
```bash
cd backend
eb init -p python-3.11 mental-health-api
eb create mental-health-api-env
```

3. **Deploy**
```bash
eb deploy
```

#### Using ECS

1. **Create ECR Repositories**
```bash
aws ecr create-repository --repository-name mental-health-backend
aws ecr create-repository --repository-name mental-health-frontend
```

2. **Push Images**
```bash
docker build -t mental-health-backend:latest backend/
docker tag mental-health-backend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/mental-health-backend:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/mental-health-backend:latest
```

3. **Create ECS Cluster and Services**
See AWS ECS documentation for detailed steps.

### NIC Cloud Deployment

1. **Register with NIC Cloud**
- Visit https://cloud.nic.in/
- Create account and project

2. **Upload Docker Images**
```bash
# Push to NIC Cloud registry
docker login -u <username> https://nic.cloud/v2/
docker build -t mental-health-backend:latest backend/
docker tag mental-health-backend:latest nic.cloud/mental-health-backend:latest
docker push nic.cloud/mental-health-backend:latest
```

3. **Deploy Services**
- Use NIC Cloud dashboard to create and manage containers
- Configure networking, storage, and environment variables

## Kubernetes Deployment

### Prerequisites
- kubectl configured
- Helm installed

### 1. Create Deployment Files
```bash
mkdir k8s
cd k8s
```

### 2. Create ConfigMap for Environment
```yaml
# config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: postgresql://user:password@postgres:5432/mental_health
  REDIS_URL: redis://redis:6379/0
  DEBUG: "False"
```

### 3. Apply Kubernetes Manifests
```bash
kubectl apply -f config.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 4. Verify Deployment
```bash
kubectl get pods
kubectl get services
kubectl logs -f deployment/mental-health-backend
```

## Production Considerations

### SSL/TLS Configuration

1. **Using Let's Encrypt**
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com

# Configure in Nginx
# See nginx.conf example
```

2. **Self-Signed Certificate (for testing)**
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

### Database Backups

1. **PostgreSQL Backup**
```bash
# Full backup
pg_dump mental_health > backup.sql

# Restore
psql mental_health < backup.sql

# Automated daily backups
0 2 * * * pg_dump mental_health > /backups/mental_health_$(date +\%Y\%m\%d).sql
```

2. **MongoDB Backup**
```bash
mongodump --db mental_health_logs --out /backups/
mongostore --db mental_health_logs /backups/mental_health_logs/
```

### Monitoring & Logging

1. **Prometheus Setup**
```bash
# Install Prometheus
docker run -d -p 9090:9090 -v prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

2. **ELK Stack Setup**
```bash
docker-compose -f elk-stack.yml up -d
```

### Performance Tuning

1. **Database Optimization**
```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM victims WHERE district='District1';

-- Create indexes
CREATE INDEX idx_victim_status ON victims(status);
CREATE INDEX idx_interaction_victim ON interactions(victim_id);
```

2. **Redis Optimization**
```bash
# Monitor Redis
redis-cli monitor

# Check memory usage
redis-cli info memory
```

3. **API Optimization**
- Enable gzip compression
- Set appropriate cache headers
- Use CDN for static assets
- Implement pagination

### Security Hardening

1. **Firewall Rules**
```bash
# Allow only required ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 80/tcp   # HTTP (redirect to HTTPS)
sudo ufw enable
```

2. **Secrets Management**
```bash
# Use environment variables
export SECRET_KEY=<your-secret-key>
export DATABASE_PASSWORD=<your-password>

# Or use secrets manager
aws secretsmanager create-secret --name mental-health/db-password
```

3. **API Rate Limiting**
- Configured in FastAPI middleware
- Adjust limits based on load testing

## Troubleshooting

### Backend Issues

1. **Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000
kill -9 <PID>
```

2. **Database Connection Error**
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Reset database
dropdb mental_health
createdb mental_health
psql -d mental_health < database/schema.sql
```

### Frontend Issues

1. **Node modules Issues**
```bash
rm -rf node_modules package-lock.json
npm install
```

2. **API Connection Errors**
- Check REACT_APP_API_URL environment variable
- Ensure backend is running
- Check CORS configuration

### Docker Issues

1. **Container won't start**
```bash
docker-compose logs <service-name>
docker-compose down
docker-compose up -d --build
```

2. **Volume permission issues**
```bash
chmod -R 755 postgres_data/
chmod -R 755 mongodb_data/
```

## Rollback Procedure

### Docker Rollback
```bash
# Revert to previous version
docker-compose down
git checkout <previous-commit>
docker-compose up -d --build
```

### Database Rollback
```bash
# Restore from backup
psql mental_health < backup.sql
```

## Maintenance

### Regular Updates
```bash
# Update Python dependencies
pip install --upgrade pip
pip install -r requirements.txt --upgrade

# Update Node dependencies
npm update
npm outdated
```

### Log Rotation
```bash
# Configure logrotate
/var/log/mental_health/*.log {
  daily
  rotate 14
  compress
  delaycompress
  notifempty
  create 0640 www-data www-data
}
```

### Health Checks
```bash
# API health
curl http://localhost:8000/health

# Database
psql -U postgres -d mental_health -c "SELECT COUNT(*) FROM victims;"
```

## Support & Escalation

For production issues:
1. Check logs: `docker-compose logs -f`
2. Verify all services: `docker-compose ps`
3. Check resource usage: `docker stats`
4. Review recent changes in git history
5. Contact system administrators with:
   - Error logs
   - Timestamp of issue
   - Recent changes made
