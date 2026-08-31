"""
Database Schema for Mental Health Monitoring System
"""

-- Victims Table
CREATE TABLE IF NOT EXISTS victims (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100),
    case_type VARCHAR(50) NOT NULL,
    case_description TEXT,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'registered',
    current_distress_score FLOAT DEFAULT 0.0,
    risk_level VARCHAR(20) DEFAULT 'low',
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_interaction_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interactions Table
CREATE TABLE IF NOT EXISTS interactions (
    id SERIAL PRIMARY KEY,
    victim_id INTEGER NOT NULL REFERENCES victims(id) ON DELETE CASCADE,
    type VARCHAR(50), -- text, voice, behavioral
    channel VARCHAR(50), -- chatbot, mobile, ivrs, sms, helpline
    content TEXT,
    audio_file_path VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis Results Table
CREATE TABLE IF NOT EXISTS analysis_results (
    id SERIAL PRIMARY KEY,
    victim_id INTEGER NOT NULL REFERENCES victims(id) ON DELETE CASCADE,
    sentiment_score FLOAT,
    emotion_detected VARCHAR(50),
    emotion_scores JSONB,
    voice_stress_score FLOAT,
    behavior_score FLOAT,
    threat_score FLOAT,
    distress_score FLOAT,
    risk_level VARCHAR(20),
    explanation TEXT,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Distress History Table
CREATE TABLE IF NOT EXISTS distress_history (
    id SERIAL PRIMARY KEY,
    victim_id INTEGER NOT NULL REFERENCES victims(id) ON DELETE CASCADE,
    score FLOAT NOT NULL,
    risk_level VARCHAR(20),
    trend VARCHAR(50), -- increasing, decreasing, stable
    record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alerts Table
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    victim_id INTEGER NOT NULL REFERENCES victims(id) ON DELETE CASCADE,
    alert_level VARCHAR(20), -- green, yellow, orange, red
    message TEXT NOT NULL,
    distress_score FLOAT,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by VARCHAR(100),
    acknowledged_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interventions Table
CREATE TABLE IF NOT EXISTS interventions (
    id SERIAL PRIMARY KEY,
    victim_id INTEGER NOT NULL REFERENCES victims(id) ON DELETE CASCADE,
    intervention_type VARCHAR(50), -- counseling, protection, financial, etc.
    status VARCHAR(50) DEFAULT 'pending', -- pending, approved, executed, completed
    notes TEXT,
    priority VARCHAR(20), -- low, medium, high
    recommended_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by VARCHAR(100),
    approved_date TIMESTAMP,
    executed_date TIMESTAMP,
    executed_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alert Recipients Table
CREATE TABLE IF NOT EXISTS alert_recipients (
    id SERIAL PRIMARY KEY,
    alert_id INTEGER NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
    recipient_type VARCHAR(50), -- counselor, district_officer, police, mental_health_specialist
    recipient_id VARCHAR(100),
    notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table (for access control)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50), -- admin, counselor, officer, specialist, viewer
    district VARCHAR(100),
    state VARCHAR(100),
    active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100),
    resource_type VARCHAR(50),
    resource_id INTEGER,
    details JSONB,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes
CREATE INDEX idx_victims_district ON victims(district);
CREATE INDEX idx_victims_state ON victims(state);
CREATE INDEX idx_victims_status ON victims(status);
CREATE INDEX idx_interactions_victim_id ON interactions(victim_id);
CREATE INDEX idx_interactions_timestamp ON interactions(timestamp);
CREATE INDEX idx_analysis_results_victim_id ON analysis_results(victim_id);
CREATE INDEX idx_distress_history_victim_id ON distress_history(victim_id);
CREATE INDEX idx_alerts_victim_id ON alerts(victim_id);
CREATE INDEX idx_alerts_level ON alerts(alert_level);
CREATE INDEX idx_interventions_victim_id ON interventions(victim_id);
CREATE INDEX idx_interventions_status ON interventions(status);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
