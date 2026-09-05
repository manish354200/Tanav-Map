# Deployment Checklist: Frontend, Backend & Database

This document provides a complete checklist for deploying the Mental Health Monitoring System across all three components.

---

## 🗄️ DATABASE DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] **PostgreSQL 15+ installed and running**
  ```bash
  postgres --version  # Check version
  pg_isready -U postgres  # Verify connection
  ```

- [ ] **Database credentials configured**
  - Database name: `mental_health`
  - User: `postgres`
  - Password: Set in `.env`
  - Host: `postgres` (Docker) or `localhost` (local)
  - Port: `5432`

- [ ] **Environment variables set in `.env`**
  ```bash
  DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/mental_health
  ```

### Database Setup
- [ ] **Initialize PostgreSQL schema**
  ```bash
  # Option 1: Using Docker (automatic)
  docker-compose up postgres
  
  # Option 2: Manual schema setup
  psql -U postgres -h localhost < database/schema.sql
  ```

- [ ] **Verify schema created**
  ```bash
  psql -U postgres -d mental_health -c "\dt"
  # Should show tables: users, victims, interactions, analysis_results, 
  #                     distress_history, alerts, interventions, audit_logs
  ```

- [ ] **Create database indices** (for performance)
  ```sql
  -- Run these to ensure indices exist
  CREATE INDEX IF NOT EXISTS idx_victims_risk_level ON victims(risk_level);
  CREATE INDEX IF NOT EXISTS idx_interactions_victim_id ON interactions(victim_id);
  CREATE INDEX IF NOT EXISTS idx_alerts_victim_id ON alerts(victim_id);
  CREATE INDEX IF NOT EXISTS idx_distress_history_victim_id ON distress_history(victim_id);
  ```

- [ ] **Test database connection**
  ```python
  from sqlalchemy import create_engine
  engine = create_engine('postgresql://postgres:password@localhost:5432/mental_health')
  connection = engine.connect()
  print("Database connected successfully!")
  connection.close()
  ```

### MongoDB Setup (Optional - Logging)
- [ ] **MongoDB 7+ running** (or Docker container)
  ```bash
  mongosh  # Connect to MongoDB shell
  db.version()  # Check version
  ```

- [ ] **Create logging database**
  ```javascript
  use mental_health_logs
  db.createCollection("audit_logs")
  db.createCollection("error_logs")
  ```

### Redis Setup (Optional - Caching)
- [ ] **Redis 7+ running** (or Docker container)
  ```bash
  redis-cli ping  # Should return PONG
  ```

### Post-Deployment Verification
- [ ] **All tables accessible**
  ```sql
  SELECT table_name FROM information_schema.tables 
  WHERE table_schema='public';
  ```

- [ ] **Foreign key constraints verified**
  ```sql
  SELECT constraint_name, table_name FROM information_schema.table_constraints 
  WHERE constraint_type='FOREIGN KEY';
  ```

- [ ] **Test data inserted (optional)**
  ```sql
  INSERT INTO users (name, email, role, password_hash) 
  VALUES ('Test User', 'test@example.com', 'admin', 'hashed_password');
  ```

---

## 🔙 BACKEND DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] **Python 3.9+ installed**
  ```bash
  python --version  # Should be 3.9 or higher
  ```

- [ ] **Virtual environment created**
  ```bash
  cd backend
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  ```

- [ ] **Dependencies installed**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Environment file configured**
  ```bash
  cp .env.example .env
  # Edit .env with actual values:
  # - DATABASE_URL
  # - SECRET_KEY (generate: openssl rand -hex 32)
  # - JWT_ALGORITHM
  # - MONGODB_URL (optional)
  # - REDIS_URL (optional)
  # - OPENROUTER_API_KEY (optional)
  ```

### Application Setup
- [ ] **Database migration completed**
  ```bash
  cd backend
  alembic upgrade head  # If using Alembic
  # OR manually run: psql -U postgres -d mental_health < database/schema.sql
  ```

- [ ] **ML models downloaded**
  ```bash
  cd ml
  python training/multilingual_setup.py
  # Downloads IndicBERT, XLM-RoBERTa, etc.
  ```

- [ ] **Application starts without errors**
  ```bash
  cd backend
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  # Should show: Uvicorn running on http://0.0.0.0:8000
  ```

### API Verification
- [ ] **Health check passes**
  ```bash
  curl http://localhost:8000/health
  # Should return: {"status": "healthy", "service": "Mental Health Monitoring System"}
  ```

- [ ] **API documentation accessible**
  ```
  Visit: http://localhost:8000/docs  (Swagger UI)
  Visit: http://localhost:8000/redoc (ReDoc)
  ```

- [ ] **Test core endpoints**
  ```bash
  # Register victim
  curl -X POST http://localhost:8000/api/v1/victims \
    -H "Content-Type: application/json" \
    -d '{"name": "Test Victim", "case_type": "test"}'
  
  # Get victims list
  curl http://localhost:8000/api/v1/victims
  
  # Submit text interaction
  curl -X POST "http://localhost:8000/api/v1/interactions/text?victim_id=1&message=I%20feel%20scared"
  ```

### Authentication Setup
- [ ] **User signup working**
  ```bash
  curl -X POST http://localhost:8000/api/v1/auth/signup \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Admin User",
      "email": "admin@example.com",
      "password": "SecurePassword123!",
      "role": "admin"
    }'
  ```

- [ ] **JWT tokens generated**
  ```bash
  curl -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@example.com&password=SecurePassword123!"
  # Should return access_token
  ```

- [ ] **Token-protected endpoints work**
  ```bash
  TOKEN="your_token_here"
  curl -H "Authorization: Bearer $TOKEN" \
    http://localhost:8000/api/v1/dashboard/district
  ```

### Performance & Monitoring
- [ ] **Database connection pool configured** (in production)
  ```python
  # backend/config/settings.py
  SQLALCHEMY_POOL_SIZE = 20
  SQLALCHEMY_POOL_RECYCLE = 3600
  SQLALCHEMY_POOL_PRE_PING = True
  ```

- [ ] **Logging configured**
  ```python
  # Logs should write to /logs directory
  # Or MongoDB for centralized logging
  ```

- [ ] **CORS configured correctly**
  ```python
  # Allow frontend domain in production
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://yourdomain.com"],  # Specify in production
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

### Production-Ready Settings
- [ ] **DEBUG mode disabled**
  ```bash
  DEBUG=False  # In .env
  ```

- [ ] **HTTPS/TLS enabled** (in production reverse proxy)
  - Use Nginx or Apache in front of Uvicorn
  - Configure SSL certificates

- [ ] **Rate limiting enabled**
  ```python
  # Use slowapi or similar library
  # Prevent abuse of ML analysis endpoints
  ```

- [ ] **Input validation strict**
  ```bash
  # Ensure Pydantic schemas validate all inputs
  # Run: pytest tests/ -v
  ```

### Deployment Method

#### Option A: Docker (Recommended)
```bash
cd backend
docker build -f ../docker/Dockerfile.backend -t mental-health-backend .
docker run -p 8000:8000 --env-file .env mental-health-backend
```

#### Option B: Manual with Gunicorn (Production)
```bash
pip install gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

#### Option C: Docker Compose (Full Stack)
```bash
docker-compose up -d backend
docker-compose logs -f backend
```

---

## 🎨 FRONTEND DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] **Node.js 16+ installed**
  ```bash
  node --version   # Should be v16 or higher
  npm --version    # Should be 8 or higher
  ```

- [ ] **Dependencies installed**
  ```bash
  cd frontend
  npm install
  # Should complete without errors
  ```

- [ ] **Environment file configured**
  ```bash
  cp .env.example .env
  # Edit .env:
  # REACT_APP_API_URL=http://localhost:8000/api/v1 (dev)
  # REACT_APP_API_URL=https://api.yourdomain.com/api/v1 (production)
  ```

### Development Testing
- [ ] **Development server runs**
  ```bash
  npm start
  # Should display: Compiled successfully!
  # Access: http://localhost:3000
  ```

- [ ] **All pages load without errors**
  - [ ] Dashboard page `/dashboard`
  - [ ] Victims list `/victims`
  - [ ] Victim details `/victim/:id`
  - [ ] Alerts page `/alerts`
  - [ ] Interventions page `/interventions`
  - [ ] Analytics page `/analytics`

- [ ] **API integration working**
  - [ ] Login/Signup form submits
  - [ ] Victims list loads from API
  - [ ] Distress scores display
  - [ ] Alerts show with correct colors
  - [ ] Charts render correctly

- [ ] **Authentication flow works**
  - [ ] Sign up new user
  - [ ] Login with credentials
  - [ ] JWT token stored in localStorage
  - [ ] Protected routes redirect to login
  - [ ] Logout clears token

### Code Quality
- [ ] **No console errors**
  ```bash
  npm start
  # Browser console should be clean (check F12)
  ```

- [ ] **Linting passes**
  ```bash
  npm run lint
  # OR: npx eslint src/
  ```

- [ ] **Build succeeds**
  ```bash
  npm run build
  # Should create /build directory
  # Check: Compiled successfully
  ```

- [ ] **Tests pass** (if configured)
  ```bash
  npm test
  # All tests should pass
  ```

### Production Build
- [ ] **Optimized build created**
  ```bash
  npm run build
  # Generates production-optimized files in /build
  # Check file sizes are reasonable
  ```

- [ ] **Build artifacts analyzed**
  ```bash
  npm run build
  # No warnings about large bundles
  # All dependencies properly bundled
  ```

- [ ] **Service worker configured** (for PWA, optional)
  ```bash
  # If using Workbox or similar
  npm run build
  ```

### Deployment Method

#### Option A: Static Hosting (AWS S3 + CloudFront)
```bash
npm run build
# Upload /build contents to S3 bucket
# Configure CloudFront distribution
# Point domain to CloudFront

# Enable GZIP compression in S3
# Set cache headers:
# - /index.html: Cache-Control: no-cache
# - /static/*: Cache-Control: max-age=31536000
```

#### Option B: Docker (Recommended)
```bash
cd frontend
docker build -f ../docker/Dockerfile.frontend -t mental-health-frontend .
docker run -p 3000:3000 --env-file .env mental-health-frontend
```

#### Option C: Nginx (Manual)
```bash
npm run build
# Copy /build to /var/www/mental-health/
# Configure nginx.conf:
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/mental-health;
    
    location / {
        try_files $uri /index.html;
    }
    
    location /api {
        proxy_pass http://backend:8000;
    }
}
```

#### Option D: Docker Compose
```bash
docker-compose up -d frontend
docker-compose logs -f frontend
```

### Production-Ready Settings
- [ ] **API base URL set to production**
  ```bash
  # .env in production
  REACT_APP_API_URL=https://api.yourdomain.com/api/v1
  ```

- [ ] **HTTPS enabled**
  - SSL certificates configured
  - Redirects HTTP → HTTPS

- [ ] **CDN configured** (optional)
  - Static assets served from CDN
  - Reduced latency for global users

- [ ] **Security headers set**
  ```
  Strict-Transport-Security: max-age=31536000
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Content-Security-Policy: default-src 'self'
  ```

- [ ] **Error tracking enabled**
  ```javascript
  // Use Sentry or similar
  import * as Sentry from "@sentry/react";
  Sentry.init({ dsn: "YOUR_DSN" });
  ```

---

## 🐳 DOCKER COMPOSE FULL STACK DEPLOYMENT

### Pre-Deployment
- [ ] **Docker installed**
  ```bash
  docker --version
  docker-compose --version
  ```

- [ ] **All `.env` files created**
  ```bash
  cp .env.example .env
  # Configure all services
  ```

- [ ] **Ports available**
  ```bash
  # Verify ports not in use:
  # 3000 (Frontend)
  # 8000 (Backend)
  # 5432 (PostgreSQL)
  # 27017 (MongoDB)
  # 6379 (Redis)
  ```

### Full Stack Deployment
- [ ] **Start all services**
  ```bash
  docker-compose up -d
  # Should start: postgres, mongodb, redis, backend, frontend
  ```

- [ ] **Verify all containers running**
  ```bash
  docker-compose ps
  # All services should show "Up"
  ```

- [ ] **Check container logs**
  ```bash
  docker-compose logs -f postgres
  docker-compose logs -f backend
  docker-compose logs -f frontend
  ```

- [ ] **Database initialized**
  ```bash
  docker-compose exec postgres psql -U postgres -d mental_health -c "\dt"
  ```

- [ ] **Backend healthy**
  ```bash
  docker-compose exec backend curl http://localhost:8000/health
  ```

- [ ] **Frontend accessible**
  ```
  Visit: http://localhost:3000
  Check: Dashboard loads, no errors
  ```

### Verification Tests
- [ ] **Full user flow works**
  1. Sign up on frontend
  2. Login with credentials
  3. Create victim
  4. Submit interaction
  5. View distress score
  6. Check alerts
  7. Logout

- [ ] **Database persistence**
  ```bash
  # Stop containers
  docker-compose down
  # Restart
  docker-compose up -d
  # Data should still exist
  ```

---

## ☁️ CLOUD DEPLOYMENT OPTIONS

### AWS Deployment
- [ ] **RDS PostgreSQL** (Managed Database)
  - Create RDS instance
  - Update `DATABASE_URL` in backend
  - Enable automated backups

- [ ] **ECS/ECR** (Container Orchestration)
  ```bash
  # Push images to ECR
  aws ecr create-repository --repository-name mental-health-backend
  docker tag mental-health-backend:latest \
    123456789.dkr.ecr.us-east-1.amazonaws.com/mental-health-backend:latest
  docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/mental-health-backend:latest
  ```

- [ ] **CloudFront** (CDN for frontend)
  - Configure S3 + CloudFront distribution
  - Set cache policies

- [ ] **ALB/NLB** (Load Balancing)
  - Create Application Load Balancer
  - Configure health checks
  - Set up target groups

### Google Cloud Deployment
- [ ] **Cloud SQL** (Managed PostgreSQL)
  - Create instance
  - Enable connections from Compute Engine
  - Set `DATABASE_URL`

- [ ] **Cloud Run** (Serverless Backend)
  ```bash
  gcloud run deploy mental-health-backend \
    --image gcr.io/PROJECT/mental-health-backend \
    --platform managed \
    --region us-central1 \
    --set-env-vars DATABASE_URL=...
  ```

- [ ] **Cloud Storage + CDN** (Frontend)
  - Upload build to GCS
  - Configure CDN

### NIC Cloud Deployment (Government)
- [ ] **Virtual Machines provisioned**
- [ ] **Private Network configured**
- [ ] **Database VM** (PostgreSQL)
- [ ] **Backend VM** (FastAPI)
- [ ] **Frontend VM** (Nginx)
- [ ] **Compliance checks** passed

---

## 🔒 Security Checklist

### Pre-Deployment Security
- [ ] **Secret management**
  - [ ] Database passwords in `.env` (not committed)
  - [ ] JWT secret generated (32+ characters)
  - [ ] API keys rotated
  - [ ] Use secrets management service (AWS Secrets Manager, etc.)

- [ ] **HTTPS/TLS enabled**
  - [ ] SSL certificates valid
  - [ ] HTTPS redirects configured
  - [ ] HSTS header set

- [ ] **Database security**
  - [ ] Accounts use strong passwords
  - [ ] SQL injection prevention (Parameterized queries)
  - [ ] Encryption at rest enabled

- [ ] **API security**
  - [ ] CORS properly configured
  - [ ] Rate limiting enabled
  - [ ] Input validation strict
  - [ ] SQL injection tests pass

- [ ] **Authentication**
  - [ ] JWT expiry set (30 mins)
  - [ ] Password hashing (bcrypt)
  - [ ] Session management secure

- [ ] **Data protection**
  - [ ] PII encrypted
  - [ ] Audit logging enabled
  - [ ] Data retention policies set
  - [ ] Compliance with Indian data protection regulations

### Post-Deployment Security
- [ ] **Penetration testing** (for production)
- [ ] **Security scanning** (OWASP Top 10)
- [ ] **Vulnerability assessments** (dependencies)
- [ ] **Regular security updates**

---

## 📊 Monitoring & Logging

### Backend Monitoring
- [ ] **Application metrics**
  ```bash
  # Prometheus endpoint
  curl http://localhost:8000/metrics
  ```

- [ ] **Error tracking**
  - Sentry integration configured
  - Alerts set up for critical errors

- [ ] **Performance monitoring**
  - Database query performance
  - API response times
  - ML model inference time

### Database Monitoring
- [ ] **Query performance**
  ```sql
  -- Check slow queries
  SELECT query, calls, mean_time 
  FROM pg_stat_statements 
  ORDER BY mean_time DESC LIMIT 10;
  ```

- [ ] **Connection pool monitoring**
- [ ] **Backup verification**
  ```bash
  # Test restore from backup
  pg_restore -d mental_health backup.sql
  ```

### Frontend Monitoring
- [ ] **Error tracking** (Sentry)
- [ ] **User analytics** (Google Analytics)
- [ ] **Performance monitoring** (Web Vitals)

### Centralized Logging
- [ ] **ELK Stack** (or Datadog)
  - Logs aggregated from all services
  - Searchable and indexed
  - Alerts configured

---

## ✅ Final Verification Checklist

### System Integration
- [ ] **End-to-end user flow works**
  1. User registers
  2. Victim created
  3. Interaction submitted
  4. Analysis triggered
  5. Distress score calculated
  6. Alert generated
  7. Intervention recommended

- [ ] **All API endpoints respond**
  ```bash
  npm run test:api  # If test script exists
  ```

- [ ] **Database queries perform**
  - List victims: < 500ms
  - Get distress score: < 200ms
  - Calculate analytics: < 1s

- [ ] **Frontend renders correctly**
  - All pages load
  - Charts display
  - Forms submit
  - Responsive design works

- [ ] **Backup and recovery work**
  ```bash
  # Test backup
  pg_dump -U postgres mental_health > backup.sql
  # Test restore
  psql -U postgres < backup.sql
  ```

### Production Readiness
- [ ] **High availability configured** (optional)
  - Database replicas
  - Backend load balancing
  - CDN for frontend

- [ ] **Disaster recovery plan**
  - Backup schedule: Daily
  - Recovery time objective (RTO): < 4 hours
  - Recovery point objective (RPO): < 1 hour

- [ ] **Scaling plan**
  - Horizontal scaling configured
  - Auto-scaling rules set
  - Load testing performed

- [ ] **Documentation complete**
  - Deployment runbook
  - Troubleshooting guide
  - Operations manual

---

## 🆘 Troubleshooting Guide

### Database Issues
```bash
# Connection refused
psql -U postgres -h localhost
# Check: PostgreSQL running? Firewall open?

# Table not found
psql -d mental_health -c "\dt"
# Check: Schema initialized? Migrations run?

# Performance slow
psql -d mental_health -c "ANALYZE;"
# Run: Vacuum and analyze
```

### Backend Issues
```bash
# ModuleNotFoundError
pip install -r requirements.txt
# Check: All dependencies installed?

# Database connection error
echo $DATABASE_URL
# Check: Env variable set? Database running?

# ML model not found
python ml/training/multilingual_setup.py
# Check: Models downloaded?

# Port 8000 already in use
lsof -i :8000
kill -9 <PID>
# OR: Use different port
```

### Frontend Issues
```bash
# Dependencies not installed
npm install
# Check: All dependencies installed?

# API not connecting
echo $REACT_APP_API_URL
# Check: Backend running? CORS configured?

# Port 3000 already in use
lsof -i :3000
kill -9 <PID>

# Build failed
npm run build
# Check: No syntax errors? All imports correct?
```

### Docker Issues
```bash
# Container won't start
docker-compose logs backend
# Check: Error messages?

# Network issues
docker network ls
docker network inspect mental_health_network
# Check: All containers on same network?

# Volume mount issues
docker-compose exec postgres ls /var/lib/postgresql/data
# Check: Data persisting to volume?
```

---

## 📞 Support & Contact

For deployment issues:
- Check logs: `docker-compose logs -f <service>`
- Review DEPLOYMENT.md in `/docs`
- Create GitHub issue with error details
- Contact project coordinators

---

**Last Updated:** 2024  
**Maintained By:** Tanav-Map Development Team
