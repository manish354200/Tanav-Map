# Mental Health Monitoring System - API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All requests require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Victim Management Endpoints

### Register Victim
**POST** `/victims`

Request body:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "gender": "Male",
  "phone_number": "+919876543210",
  "email": "john@example.com",
  "case_type": "rape",
  "case_description": "Case details...",
  "district": "District Name",
  "state": "State Name"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "status": "registered",
  "current_distress_score": 50.0,
  "risk_level": "medium",
  "registration_date": "2024-01-15T10:30:00"
}
```

### List Victims
**GET** `/victims?page=1&page_size=10&status=registered&district=District`

Query Parameters:
- `page` (default: 1) - Page number
- `page_size` (default: 10) - Items per page
- `status` (optional) - Filter by status
- `district` (optional) - Filter by district

Response:
```json
{
  "total": 156,
  "page": 1,
  "page_size": 10,
  "items": [...]
}
```

### Get Victim Details
**GET** `/victims/{victim_id}`

Response:
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "status": "registered",
  "current_distress_score": 68,
  "risk_level": "high",
  ...
}
```

### Update Victim
**PUT** `/victims/{victim_id}`

Request body:
```json
{
  "status": "under_investigation",
  "phone_number": "+919876543211"
}
```

### Delete Victim
**DELETE** `/victims/{victim_id}`

## Data Collection Endpoints

### Log Text Interaction
**POST** `/interactions/text`

Request body:
```json
{
  "victim_id": 1,
  "message": "I am scared to go outside.",
  "channel": "chatbot"
}
```

Response:
```json
{
  "interaction_id": 101,
  "status": "received",
  "message": "Text interaction logged successfully"
}
```

### Upload Voice Recording
**POST** `/interactions/voice`

Multipart form data:
- `victim_id` (form field)
- `file` (audio file)
- `channel` (form field, e.g., "ivrs")

### Get Interaction History
**GET** `/interactions/{victim_id}/history?limit=10`

Response:
```json
{
  "victim_id": 1,
  "total_interactions": 45,
  "recent_interactions": [...]
}
```

## Analysis Endpoints

### Trigger Analysis
**POST** `/analysis/{victim_id}/analyze`

Response:
```json
{
  "victim_id": 1,
  "analysis": {
    "sentiment_score": 65,
    "sentiment": "Negative",
    "emotion": "Anxiety",
    "emotion_scores": {...},
    "voice_stress": 0.72
  },
  "distress_score": {
    "current": 68,
    "risk_level": "high"
  },
  "explanation": ["Fear keywords increased 35%", ...]
}
```

### Get Current Distress Score
**GET** `/analysis/{victim_id}/distress-score`

Response:
```json
{
  "victim_id": 1,
  "current_score": 68,
  "risk_level": "high",
  "last_updated": "2024-01-15T10:30:00",
  "trend": "increasing"
}
```

### Get Distress Trend
**GET** `/analysis/{victim_id}/distress-trend?days=30`

Response:
```json
{
  "victim_id": 1,
  "period_days": 30,
  "trend": [
    {
      "days_ago": 30,
      "score": 50,
      "risk_level": "low"
    },
    ...
  ],
  "prediction": {
    "7_day_risk": 75,
    "15_day_risk": 82,
    "30_day_risk": 88
  }
}
```

## Alert Endpoints

### Get All Alerts
**GET** `/alerts?status=pending&level=high&limit=20`

Query Parameters:
- `status` - "pending" or "acknowledged"
- `level` - "green", "yellow", "orange", "red"
- `limit` - number of alerts to return

### Get Alert Details
**GET** `/alerts/{alert_id}`

### Acknowledge Alert
**POST** `/alerts/{alert_id}/acknowledge`

Response:
```json
{
  "message": "Alert acknowledged",
  "alert_id": 1,
  "timestamp": "2024-01-15T10:30:00"
}
```

## Intervention Endpoints

### Get Recommended Interventions
**GET** `/interventions/{victim_id}`

Response:
```json
{
  "victim_id": 1,
  "distress_score": 72,
  "recommendations": [
    {
      "type": "counseling",
      "priority": "high",
      "description": "Recommended counseling intervention",
      "status": "pending"
    }
  ]
}
```

### Create Intervention
**POST** `/interventions/{victim_id}/recommend`

Request body:
```json
{
  "intervention_type": "counseling",
  "notes": "Weekly counseling sessions recommended"
}
```

### Approve Intervention
**POST** `/interventions/{intervention_id}/approve`

Request body:
```json
{
  "approved_by": "counselor_001"
}
```

### Execute Intervention
**POST** `/interventions/{intervention_id}/execute`

## Dashboard Endpoints

### District Dashboard
**GET** `/dashboard/district?district=District Name`

Response:
```json
{
  "level": "district",
  "statistics": {
    "total_victims": 156,
    "high_risk_victims": 12,
    "new_alerts_today": 3
  }
}
```

### State Dashboard
**GET** `/dashboard/state?state=State Name`

### National Dashboard
**GET** `/dashboard/national`

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- Rate limit: 100 requests per minute per IP
- Rate limit header: `X-RateLimit-Remaining`

## Webhooks

The system supports webhooks for:
- High-risk alert notifications
- Intervention status changes
- Distress score updates

Configure webhooks in the admin panel.
