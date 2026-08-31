import React from 'react';

const Alerts = () => {
  return (
    <div className="alerts-page">
      <h1>Active Alerts</h1>
      
      <div className="alert-filters">
        <button className="filter-btn active">All</button>
        <button className="filter-btn">Critical (Red)</button>
        <button className="filter-btn">High (Orange)</button>
        <button className="filter-btn">Medium (Yellow)</button>
      </div>

      <div className="alerts-container">
        <div className="alert-item critical">
          <div className="alert-header">
            <span className="alert-level">CRITICAL</span>
            <span className="alert-time">2 hours ago</span>
          </div>
          <div className="alert-content">
            <h3>Severe Mental Health Crisis Detected</h3>
            <p>Victim ID: #1001</p>
            <p>Distress Score: 88/100</p>
            <p className="alert-message">Multiple threat keywords detected. Immediate psychiatric intervention recommended.</p>
          </div>
          <div className="alert-actions">
            <button className="btn-primary">View Details</button>
            <button className="btn-secondary">Acknowledge</button>
          </div>
        </div>

        {/* More alert items */}
      </div>
    </div>
  );
};

export default Alerts;
