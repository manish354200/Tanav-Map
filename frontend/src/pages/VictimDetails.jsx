import React from 'react';

const VictimDetails = () => {
  return (
    <div className="victim-details">
      <div className="victim-header">
        <h1>Victim Profile</h1>
        <div className="status-badge">Registered</div>
      </div>

      <div className="details-grid">
        <div className="details-card">
          <h2>Personal Information</h2>
          <div className="info-row">
            <label>Name:</label>
            <span>Sample Victim Name</span>
          </div>
          <div className="info-row">
            <label>Case Type:</label>
            <span>Gang Rape</span>
          </div>
          <div className="info-row">
            <label>Registration Date:</label>
            <span>2024-01-01</span>
          </div>
        </div>

        <div className="details-card">
          <h2>Mental Health Status</h2>
          <div className="distress-score">
            <h3>Current Distress Score: <span className="score-value danger">72</span>/100</h3>
            <div className="risk-indicator">
              <span className="risk-level">High Risk</span>
            </div>
          </div>
        </div>

        <div className="details-card">
          <h2>Distress Trend</h2>
          {/* Chart component */}
        </div>

        <div className="details-card">
          <h2>Recommendations</h2>
          <ul>
            <li>Counseling session scheduled</li>
            <li>Psychiatric referral recommended</li>
            <li>Witness protection needed</li>
          </ul>
        </div>

        <div className="details-card">
          <h2>Recent Interactions</h2>
          <ul>
            {/* Interaction list */}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default VictimDetails;
