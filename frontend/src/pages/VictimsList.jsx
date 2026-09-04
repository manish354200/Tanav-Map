import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { victimAPI } from '../services/api';
import { useLanguage } from '../i18n';

const VictimsList = () => {
  const { t } = useLanguage();
  const [victims, setVictims] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVictims = async () => {
      try {
        const response = await victimAPI.getAll(1, 20);
        setVictims(response?.data?.items || []);
      } catch (error) {
        console.error('Failed to fetch victims:', error);
        setVictims([]);
      } finally {
        setLoading(false);
      }
    };

    fetchVictims();
  }, []);

  return (
    <div className="victims-list">
      <h1>{t('victims')}</h1>
      <div className="filter-section">
        <input type="text" placeholder="Search by name or ID..." />
        <select>
          <option>All Status</option>
          <option>Registered</option>
          <option>Under Investigation</option>
          <option>Trial Ongoing</option>
        </select>
        <select>
          <option>All Risks</option>
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
          <option>Critical</option>
        </select>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Case Type</th>
              <th>Status</th>
              <th>Distress Score</th>
              <th>Risk Level</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="7">Loading victims...</td>
              </tr>
            ) : victims.length > 0 ? (
              victims.map((victim) => (
                <tr key={victim.id}>
                  <td>#{victim.id}</td>
                  <td>{victim.name || 'Unnamed Victim'}</td>
                  <td>{victim.case_type || 'Not specified'}</td>
                  <td>{victim.status || 'registered'}</td>
                  <td>{victim.current_distress_score ?? '--'}</td>
                  <td>{victim.risk_level || 'medium'}</td>
                  <td>
                    <Link to={`/victims/${victim.id}`}>View</Link>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7">No victims found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VictimsList;
