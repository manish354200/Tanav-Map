import React from 'react';

const Navbar = ({ session, onLogout }) => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>Mental Health Monitoring System</h1>
      </div>
      <div className="navbar-menu">
        <a href="/" className="nav-item">Home</a>
        <a href="/dashboard" className="nav-item">Dashboard</a>
        <a href="/alerts" className="nav-item">Alerts</a>
        <a href="/help" className="nav-item">Help</a>
      </div>
      <div className="navbar-user">
        <span className="user-name">{session?.name || session?.email}</span>
        <button className="btn-logout" onClick={onLogout}>Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;
