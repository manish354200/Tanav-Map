import React, { useEffect, useState } from 'react';
import { alertAPI } from '../services/api';
import { useLanguage } from '../i18n';

const Alerts = () => {
  const { t } = useLanguage();
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await alertAPI.getAll('', '', 20);
        setAlerts(response?.data?.alerts || []);
      } catch (error) {
        console.error('Failed to fetch alerts:', error);
        setAlerts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  return (
    <div className="alerts-page">
      <h1>{t('activeAlerts')}</h1>

      <div className="alert-filters">
        <button className="filter-btn active">All</button>
        <button className="filter-btn">Critical (Red)</button>
        <button className="filter-btn">High (Orange)</button>
        <button className="filter-btn">Medium (Yellow)</button>
      </div>

      <div className="alerts-container">
        {loading ? (
          <p>Loading alerts...</p>
        ) : alerts.length > 0 ? (
          alerts.map((alert, index) => (
            <div key={alert.id || index} className={`alert-item ${alert.level || 'info'}`}>
              <div className="alert-header">
                <span className="alert-level">{(alert.level || 'INFO').toUpperCase()}</span>
                <span className="alert-time">{alert.created_at || 'recently'}</span>
              </div>
              <div className="alert-content">
                <h3>{alert.title || 'Mental Health Alert'}</h3>
                <p>Victim ID: #{alert.victim_id || 'N/A'}</p>
                <p>Distress Score: {alert.score || 'N/A'}/100</p>
                <p className="alert-message">
                  {alert.message || 'Priority intervention recommended.'}
                </p>
              </div>
              <div className="alert-actions">
                <button className="btn-primary">View Details</button>
                <button className="btn-secondary">Acknowledge</button>
              </div>
            </div>
          ))
        ) : (
          <p>No alerts currently reported.</p>
        )}
      </div>
    </div>
  );
};

export default Alerts;
