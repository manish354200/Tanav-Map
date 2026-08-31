import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { analysisAPI, interactionAPI, victimAPI } from '../services/api';

const VictimDetails = () => {
  const { id } = useParams();
  const [victim, setVictim] = useState(null);
  const [history, setHistory] = useState([]);
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVictimData = async () => {
      try {
        const [victimResponse, historyResponse, scoreResponse] = await Promise.all([
          victimAPI.get(id),
          interactionAPI.getHistory(id, 5),
          analysisAPI.getDistressScore(id),
        ]);

        setVictim(victimResponse?.data || null);
        setHistory(historyResponse?.data?.recent_interactions || []);
        setScore(scoreResponse?.data || null);
      } catch (error) {
        console.error('Failed to fetch victim details:', error);
        setVictim(null);
        setHistory([]);
        setScore(null);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchVictimData();
  }, [id]);

  if (loading) return <div className="victim-details"><h1>Loading victim profile...</h1></div>;
  if (!victim) return <div className="victim-details"><h1>Victim not found</h1></div>;

  return (
    <div className="victim-details">
      <div className="victim-header">
        <h1>Victim Profile</h1>
        <div className="status-badge">{victim.status || 'Registered'}</div>
      </div>

      <div className="details-grid">
        <div className="details-card">
          <h2>Personal Information</h2>
          <div className="info-row">
            <label>Name:</label>
            <span>{victim.name || 'Unnamed Victim'}</span>
          </div>
          <div className="info-row">
            <label>Case Type:</label>
            <span>{victim.case_type || 'Not specified'}</span>
          </div>
          <div className="info-row">
            <label>Registration Date:</label>
            <span>{victim.registration_date || 'N/A'}</span>
          </div>
        </div>

        <div className="details-card">
          <h2>Mental Health Status</h2>
          <div className="distress-score">
            <h3>
              Current Distress Score:{' '}
              <span className="score-value danger">{score?.current_score ?? victim.current_distress_score ?? 0}</span>/100
            </h3>
            <div className="risk-indicator">
              <span className="risk-level">{score?.risk_level || victim.risk_level || 'Medium'}</span>
            </div>
          </div>
        </div>

        <div className="details-card">
          <h2>Distress Trend</h2>
          <div className="trend-bars">
            {[38, 42, 55, 63, 70, 68, 74].map((value, index) => (
              <div key={index} className="trend-bar" style={{ height: `${value}%` }} title={`Trend ${value}`} />
            ))}
          </div>
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
            {history.length > 0 ? (
              history.map((item, index) => (
                <li key={item.id || index}>{item.message || 'Interaction recorded'}</li>
              ))
            ) : (
              <li>No recent interactions recorded.</li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default VictimDetails;
