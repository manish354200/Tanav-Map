import React from 'react';
import { useLanguage } from '../i18n';

const Navbar = ({ session, onLogout }) => {
  const { language, setLanguage, languageOptions, t } = useLanguage();
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>{t('appName')}</h1>
      </div>
      <div className="navbar-menu">
        <a href="/" className="nav-item">{t('home')}</a>
        <a href="/dashboard" className="nav-item">{t('dashboard')}</a>
        <a href="/alerts" className="nav-item">{t('alerts')}</a>
        <a href="/help" className="nav-item">{t('help')}</a>
      </div>
      <div className="navbar-user">
        <span className="user-name">{session?.name || session?.email}</span>
        <label className="navbar-language">
          <span className="sr-only">{t('languageLabel')}</span>
          <select value={language} onChange={(event) => setLanguage(event.target.value)} aria-label={t('languageLabel')}>
            {languageOptions.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
          </select>
        </label>
        <button className="btn-logout" onClick={onLogout}>{t('logout')}</button>
      </div>
    </nav>
  );
};

export default Navbar;
