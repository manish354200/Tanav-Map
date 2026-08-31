# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Users/Interface Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Dashboard  │  │    Mobile    │  │   Chatbot    │          │
│  │  (React)     │  │   (Flutter)  │  │   Interface  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                        API Layer (FastAPI)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Authentication │ Routing │ Validation │ Rate Limiting  │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                    Business Logic Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Victim Mgmt │  │ Data Process │  │ Scoring &    │          │
│  │   Service    │  │   Service    │  │ Prediction   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                    AI/ML Analysis Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Sentiment   │  │   Emotion    │  │   Voice      │          │
│  │  Analysis    │  │  Detection   │  │  Analytics   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Behavioral   │  │ Threat       │  │ Prediction   │          │
│  │ Analytics    │  │ Detection    │  │ Models       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                   Data Layer                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  PostgreSQL  │  │   MongoDB    │  │    Redis     │          │
│  │   (Primary)  │  │    (Logs)    │  │  (Cache)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer
- **Dashboard** (React): District, State, and National level dashboards
- **Mobile App** (Flutter): On-the-go victim monitoring
- **Chatbot Interface**: For victim interactions
- **IVRS Integration**: Voice-based data collection

### 2. API Layer (FastAPI)
- RESTful endpoints for all operations
- JWT-based authentication
- Role-based access control (RBAC)
- Rate limiting and request validation
- Comprehensive error handling
- API versioning (/api/v1, etc.)

### 3. Business Logic Layer
- **Victim Management**: CRUD operations, status tracking
- **Data Processing**: Text preprocessing, audio processing
- **Scoring & Prediction**: Distress score calculation, risk prediction
- **Intervention Engine**: Recommendation generation
- **Alert System**: Alert creation and routing

### 4. AI/ML Analysis Layer
- **Sentiment Analysis**: Classify positive/neutral/negative emotions
- **Emotion Detection**: Identify specific emotions (fear, anxiety, etc.)
- **Voice Analytics**: Analyze voice stress, pitch, speech patterns
- **Behavioral Analytics**: Track engagement patterns, missed interactions
- **Threat Detection**: Identify keywords indicating threats
- **Prediction Models**: Forecast 7/15/30-day distress trends

### 5. Data Layer
- **PostgreSQL**: Primary relational database
  - Victim profiles
  - Interactions and analysis results
  - Alerts and interventions
  - User management and audit logs
- **MongoDB**: Event and log storage
  - Raw interaction logs
  - Analysis raw data
  - Application logs
- **Redis**: Caching and session management
  - Distress scores cache
  - User sessions
  - Rate limiting counters

## Data Flow

### Victim Interaction Flow
```
1. Victim Interaction (Text/Voice)
   ↓
2. API Receives Data
   ↓
3. Preprocessing & Validation
   ↓
4. AI Analysis (Sentiment, Emotion, Voice, Behavior)
   ↓
5. Calculate Distress Score
   ↓
6. Generate Recommendations
   ↓
7. Create Alerts if needed
   ↓
8. Store in Database
   ↓
9. Update Dashboard
   ↓
10. Notify Counselors (if needed)
```

### Alert & Intervention Flow
```
1. High Distress Score Detected
   ↓
2. Determine Alert Level (Green/Yellow/Orange/Red)
   ↓
3. Create Alert
   ↓
4. Route to Recipients (Counselors, Officers, etc.)
   ↓
5. Send Notifications
   ↓
6. Generate Intervention Recommendations
   ↓
7. Route to Counselor for Approval (Human-in-the-Loop)
   ↓
8. On Approval, Update Status
   ↓
9. Track Execution
```

## Security Architecture

### Authentication
- JWT tokens for API authentication
- Refresh token mechanism
- Session-based login for web dashboard

### Authorization
- Role-Based Access Control (RBAC)
  - Admin: Full system access
  - Counselor: Manage assigned victims
  - Officer: View district/state data
  - Specialist: Mental health specific functions
  - Viewer: Read-only access

### Data Protection
- End-to-end encryption for communications
- Database encryption at rest
- Field-level encryption for sensitive data
- Data anonymization in logs
- Secure password hashing (bcrypt)

### Audit & Compliance
- Complete audit logs for all actions
- GDPR compliance measures
- Indian data protection law compliance
- Regular security audits
- Incident logging and reporting

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- Caching layer (Redis)
- Load balancing

### Vertical Scaling
- Database query optimization
- Asynchronous processing (Celery)
- Model optimization
- Batch processing for reports

### Performance Optimization
- Database indexing strategy
- Redis caching for frequent queries
- API response caching
- Lazy loading for UI components
- Pagination for large datasets

## Deployment Architecture

### Development
- Local docker-compose setup
- SQLite for quick testing
- Hot-reload enabled

### Production
- Kubernetes orchestration
- Multiple replicas for high availability
- Database backups and replication
- SSL/TLS for all communications
- CDN for static assets
- Logging and monitoring (Prometheus, ELK)

### Cloud Options
- NIC Cloud (Government recommended)
- AWS (VPC, RDS, ElastiCache)
- On-premise deployment supported

## Monitoring & Logging

### Application Monitoring
- Prometheus metrics
- Real-time performance dashboards
- Alert thresholds
- Health checks

### Logging
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Centralized log aggregation
- Log retention policies
- Searchable logs for debugging

### Error Tracking
- Sentry for error monitoring
- Error rate tracking
- Stack trace preservation
- Automatic alerts for critical errors
