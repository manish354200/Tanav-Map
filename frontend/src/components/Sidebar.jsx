import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-menu">
        <Link to="/dashboard" className="menu-item">
          <span className="icon">📊</span> Dashboard
        </Link>
        <Link to="/victims" className="menu-item">
          <span className="icon">👥</span> Victims
        </Link>
        <Link to="/alerts" className="menu-item">
          <span className="icon">🚨</span> Alerts
        </Link>
        <Link to="/interventions" className="menu-item">
          <span className="icon">💡</span> Interventions
        </Link>
        <Link to="/analytics" className="menu-item">
          <span className="icon">📈</span> Analytics
        </Link>
      </div>
    </aside>
  );
};

export default Sidebar;
