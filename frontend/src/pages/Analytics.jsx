import React from 'react';
import { useLanguage } from '../i18n';

const Analytics = () => {
  const { t } = useLanguage();
  return (
    <div className="analytics-page">
      <h1>{t('analytics')}</h1>
      
      <div className="analytics-grid">
        <div className="analytics-card">
          <h2>Distress Distribution by Risk Level</h2>
          {/* Pie chart */}
        </div>
        
        <div className="analytics-card">
          <h2>Case Type Distribution</h2>
          {/* Bar chart */}
        </div>
        
        <div className="analytics-card">
          <h2>Intervention Success Rate</h2>
          {/* Line chart */}
        </div>
        
        <div className="analytics-card">
          <h2>Alert Trends</h2>
          {/* Area chart */}
        </div>
      </div>

      <div className="report-section">
        <h2>Generate Report</h2>
        <button className="btn-primary">Download District Report (PDF)</button>
        <button className="btn-primary">Download State Report (PDF)</button>
        <button className="btn-primary">Download National Report (PDF)</button>
      </div>
    </div>
  );
};

export default Analytics;
