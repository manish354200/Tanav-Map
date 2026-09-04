import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../i18n';

const Sidebar = () => {
  const { t } = useLanguage();
  return (
    <aside className="sidebar">
      <div className="sidebar-menu">
        <Link to="/dashboard" className="menu-item">
          <span className="icon">📊</span> {t('dashboard')}
        </Link>
        <Link to="/victims" className="menu-item">
          <span className="icon">👥</span> {t('victims')}
        </Link>
        <Link to="/alerts" className="menu-item">
          <span className="icon">🚨</span> {t('alerts')}
        </Link>
        <Link to="/interventions" className="menu-item">
          <span className="icon">💡</span> {t('interventions')}
        </Link>
        <Link to="/analytics" className="menu-item">
          <span className="icon">📈</span> {t('analytics')}
        </Link>
      </div>
    </aside>
  );
};

export default Sidebar;
