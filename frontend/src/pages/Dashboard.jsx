import React from 'react';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <h1>Mental Health Monitoring Dashboard</h1>
      <div className="dashboard-grid">
        <div className="stat-card">
          <h3>Total Victims</h3>
          <p className="stat-value">156</p>
        </div>
        <div className="stat-card">
          <h3>High Risk Cases</h3>
          <p className="stat-value danger">12</p>
        </div>
        <div className="stat-card">
          <h3>Active Alerts</h3>
          <p className="stat-value warning">8</p>
        </div>
        <div className="stat-card">
          <h3>Interventions Today</h3>
          <p className="stat-value success">5</p>
        </div>
      </div>
      
      <div className="dashboard-section">
        <h2>Recent Alerts</h2>
        <div className="alert-list">
          {/* Alert items will be rendered here */}
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Distress Trend</h2>
        <div className="chart-container">
          {/* Recharts component will go here */}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
