import React from 'react';

const VictimsList = () => {
  return (
    <div className="victims-list">
      <h1>Victims Registry</h1>
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
            {/* Victim rows will be rendered here */}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VictimsList;
