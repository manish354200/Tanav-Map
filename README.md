# AI-Based Dynamic Mental Health Monitoring & Distress Prediction System

## Overview
An intelligent system for continuous monitoring and predicting psychological distress among victims and complainants throughout investigation, trial, rehabilitation, and compensation processes.

## System Architecture

### Layer 1: Data Collection
- **Channels**: Chatbot, Mobile App, IVRS, SMS, Helpline follow-ups
- **Data Types**: Text, Voice, Behavior patterns

### Layer 2: AI Analysis Engine
- **Sentiment Analysis** - Classify positive/neutral/negative emotions
- **Emotion Detection** - Identify fear, anxiety, anger, sadness, stress using multilingual models (IndicBERT, MuRIL, XLM-RoBERTa)
- **Voice Stress Analytics** - Analyze pitch, tremor, speaking speed, pauses
- **Behavioral Analytics** - Track missed follow-ups, response delays, engagement patterns

### Layer 3: Distress Scoring & Prediction
- **Dynamic Distress Score (DDS)** - Weighted scoring (0-100 scale)
  - Sentiment: 30%, Voice: 25%, Behavior: 20%, Threats: 15%, History: 10%
- **Risk Categories**: Low (0-30), Medium (31-60), High (61-80), Critical (81-100)
- **Predictive Models**: XGBoost, LightGBM, LSTM for 7/15/30-day forecasting

### Layer 4: Intervention & Alerts
- **Alert Levels**: Green (Normal), Yellow (Medium Risk), Orange (High Risk), Red (Critical)
- **Automated Recommendations**: Counseling, witness protection, financial assistance, relocation support
- **Intervention Routing**: Counsellors → District Officers → Police/Mental Health Specialists

### Layer 5: Dashboards
- District, State, and National level monitoring dashboards
- High-risk victim identification
- Resource allocation recommendations

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (primary), MongoDB (logs/events)
- **Authentication**: JWT, Role-based access control

### Frontend
- **Framework**: React.js
- **UI Library**: Material-UI or Tailwind CSS
- **Mobile**: Flutter (optional)
- **State Management**: Redux

### ML/AI
- **NLP Models**: IndicBERT, MuRIL, XLM-RoBERTa, Whisper (voice)
- **Voice Analytics**: OpenSMILE, Librosa
- **ML Models**: XGBoost, LightGBM, LSTM, Scikit-learn
- **Explainability**: SHAP, LIME

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes (optional)
- **Cloud**: NIC Cloud, AWS, or on-premise
- **Monitoring**: Prometheus, ELK Stack

## Project Structure

```
sih/
├── backend/
│   ├── app/
│   │   ├── models/           # Database models & ML models
│   │   ├── services/         # Business logic (analysis, predictions)
│   │   ├── routes/           # API endpoints
│   │   ├── schemas/          # Pydantic schemas for validation
│   │   ├── middleware/       # Auth, logging, error handling
│   │   └── utils/            # Helper functions
│   ├── config/               # Configuration management
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client services
│   │   ├── hooks/           # Custom React hooks
│   │   ├── store/           # Redux store
│   │   └── App.jsx          # Main app component
│   ├── package.json         # Dependencies
│   └── .env.example         # Environment variables template
├── ml/
│   ├── models/              # Pre-trained models
│   ├── training/            # Training scripts
│   ├── notebooks/           # Jupyter notebooks for EDA
│   └── requirements.txt     # ML-specific dependencies
├── database/
│   ├── schema.sql           # Database schema
│   ├── migrations/          # Database migrations
│   └── seeds/               # Seed data
├── docker/
│   ├── Dockerfile.backend   # Backend container
│   ├── Dockerfile.frontend  # Frontend container
│   └── docker-compose.yml   # Multi-container orchestration
├── docs/
│   ├── API.md              # API documentation
│   ├── DEPLOYMENT.md       # Deployment guide
│   ├── ARCHITECTURE.md     # System architecture details
│   └── CONTRIBUTING.md     # Contribution guidelines
└── tests/                  # Unit and integration tests
```

## Key Features

### 1. **Continuous Monitoring**
- Real-time victim interaction tracking
- Multi-channel data ingestion

### 2. **Advanced AI Analysis**
- Multilingual support (Hindi, Tamil, Telugu, Bengali, Marathi, Punjabi, etc.)
- Emotion and sentiment detection
- Voice stress analytics
- Behavioral pattern analysis

### 3. **Predictive Analytics**
- Early crisis detection
- Distress trajectory forecasting
- Threat level assessment

### 4. **Intelligent Alerts**
- Risk-based alert routing
- Real-time notifications
- Action recommendations

### 5. **Explainable AI**
- Transparent risk scoring
- Decision explainability for government compliance
- Audit trail for all recommendations

### 6. **Security & Privacy**
- End-to-end encryption
- Role-based access control (RBAC)
- Data anonymization
- GDPR & local law compliance
- Complete audit logs

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Docker & Docker Compose

### Installation

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

#### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
```

#### Database Setup
```bash
cd database
psql -U postgres < schema.sql
```

### Running the Application

#### Using Docker (Recommended)
```bash
docker-compose up -d
```

#### Manual Setup
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: Database
# Ensure PostgreSQL is running
```

### Access the Application
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Dashboard: http://localhost:3000/dashboard

## API Endpoints

### Victim Management
- `POST /api/v1/victims` - Register new victim
- `GET /api/v1/victims/{id}` - Get victim details
- `PUT /api/v1/victims/{id}` - Update victim profile

### Data Collection
- `POST /api/v1/interactions` - Log victim interaction
- `POST /api/v1/voice-data` - Upload voice recording
- `POST /api/v1/text-feedback` - Submit text feedback

### Analysis & Scoring
- `GET /api/v1/distress-score/{victim_id}` - Get current distress score
- `GET /api/v1/distress-trend/{victim_id}` - Get distress history
- `POST /api/v1/analyze` - Trigger analysis on new data

### Dashboards
- `GET /api/v1/dashboard/district` - District-level statistics
- `GET /api/v1/dashboard/state` - State-level statistics
- `GET /api/v1/dashboard/national` - National-level statistics

### Alerts & Interventions
- `GET /api/v1/alerts` - Get active alerts
- `GET /api/v1/interventions/{victim_id}` - Get intervention recommendations
- `POST /api/v1/interventions/{victim_id}/acknowledge` - Acknowledge intervention

## Development

### Running Tests
```bash
cd backend
pytest tests/

cd frontend
npm test
```

### Code Quality
```bash
# Backend linting
flake8 app/
black app/

# Frontend linting
npm run lint
npm run format
```

### Database Migrations
```bash
alembic upgrade head
```

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for:
- Cloud deployment instructions
- Kubernetes configuration
- CI/CD pipeline setup
- Monitoring and logging

## Innovation Highlights

1. **Distress Trajectory Graph** - Predict future emotional decline
2. **Threat Detection Model** - Detect intimidation and harassment
3. **Multilingual Indian Support** - Support for 6+ Indian languages
4. **AI Case Prioritization** - Rank victims by intervention urgency
5. **Human-in-the-Loop AI** - Counselors approve all interventions
6. **Explainable AI** - Government-compliant transparency

## Security Considerations

- All data transmitted via HTTPS/TLS
- End-to-end encryption for sensitive communications
- Database encryption at rest
- Regular security audits
- Compliance with Indian data protection regulations
- Complete audit logging for accountability

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is developed for the Software Innovation Hackathon (SIH) and follows applicable government regulations.

## Contact & Support

- **Documentation**: See `/docs` folder
- **Issues**: Use GitHub Issues for bug reports
- **Support**: Contact project coordinators for assistance

## Acknowledgments

Developed as part of the National Mission on Mental Health and Victim Support Initiative.
