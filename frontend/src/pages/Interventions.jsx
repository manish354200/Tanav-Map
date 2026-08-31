import React from 'react';

const Interventions = () => {
  return (
    <div className="interventions-page">
      <h1>Intervention Management</h1>
      
      <div className="intervention-filters">
        <select>
          <option>All Status</option>
          <option>Pending</option>
          <option>Approved</option>
          <option>Executed</option>
        </select>
        <select>
          <option>All Types</option>
          <option>Counseling</option>
          <option>Witness Protection</option>
          <option>Financial Assistance</option>
          <option>Relocation Support</option>
        </select>
      </div>

      <div className="interventions-list">
        <div className="intervention-card">
          <div className="intervention-header">
            <h3>Counseling Session</h3>
            <span className="status-badge pending">Pending Approval</span>
          </div>
          <div className="intervention-body">
            <p><strong>Victim:</strong> ID #1001</p>
            <p><strong>Priority:</strong> High</p>
            <p><strong>Created:</strong> 2024-01-15 10:30</p>
            <p><strong>Reason:</strong> Elevated anxiety and stress indicators detected</p>
          </div>
          <div className="intervention-actions">
            <button className="btn-approve">Approve</button>
            <button className="btn-reject">Reject</button>
          </div>
        </div>

        {/* More intervention cards */}
      </div>
    </div>
  );
};

export default Interventions;
