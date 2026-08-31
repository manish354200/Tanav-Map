import React, { useEffect, useState } from 'react';
import { dashboardAPI, alertAPI } from '../services/api';
import SupportAssistant from '../components/SupportAssistant';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalVictims: 0,
    highRiskCases: 0,
    activeAlerts: 0,
    interventionsToday: 5,
  });
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [nationalResponse, alertsResponse] = await Promise.all([
          dashboardAPI.getNational(),
          alertAPI.getAll('', '', 5),
        ]);

        const nationalStats = nationalResponse?.data?.statistics || {};
        const alertList = alertsResponse?.data?.alerts || [];

        setStats({
          totalVictims: nationalStats.total_victims || 0,
          highRiskCases: nationalStats.high_risk_victims || 0,
          activeAlerts: alertList.length,
          interventionsToday: 5,
        });
        setAlerts(alertList);
        setError('');
      } catch (err) {
        console.error('Dashboard data fetch failed:', err);
        setError('Unable to load dashboard data right now.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="dashboard">
      <h1>Mental Health Monitoring Dashboard</h1>

      {error && <p className="error-message">{error}</p>}

      <div className="dashboard-grid">
        <div className="stat-card">
          <h3>Total Victims</h3>
          <p className="stat-value">{loading ? '...' : stats.totalVictims}</p>
        </div>
        <div className="stat-card">
          <h3>High Risk Cases</h3>
          <p className="stat-value danger">{loading ? '...' : stats.highRiskCases}</p>
        </div>
        <div className="stat-card">
          <h3>Active Alerts</h3>
          <p className="stat-value warning">{loading ? '...' : stats.activeAlerts}</p>
        </div>
        <div className="stat-card">
          <h3>Interventions Today</h3>
          <p className="stat-value success">{loading ? '...' : stats.interventionsToday}</p>
        </div>
      </div>

      <SupportAssistant />

      <div className="dashboard-section">
        <h2>Recent Alerts</h2>
        <div className="alert-list">
          {loading ? (
            <p>Loading alerts...</p>
          ) : alerts.length > 0 ? (
            alerts.map((alert) => (
              <div key={alert.id || alert.victim_id || Math.random()} className="alert-item">
                <strong>{alert.level || 'info'}</strong>
                <span>{alert.message || 'Alert received'}</span>
              </div>
            ))
          ) : (
            <p>No alerts currently reported.</p>
          )}
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Distress Trend</h2>
        <div className="chart-container">
          <div className="trend-bars">
            {[42, 48, 51, 58, 62, 66, 72].map((value, index) => (
              <div key={index} className="trend-bar" style={{ height: `${value}%` }} title={`Score ${value}`} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
