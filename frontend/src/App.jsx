import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store';

// Pages
import Dashboard from './pages/Dashboard';
import VictimsList from './pages/VictimsList';
import VictimDetails from './pages/VictimDetails';
import Alerts from './pages/Alerts';
import Interventions from './pages/Interventions';
import Analytics from './pages/Analytics';
import Auth from './pages/Auth';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

function App() {
  const [session, setSession] = React.useState(() => {
    const savedSession = localStorage.getItem('mental-health-session');
    return savedSession ? JSON.parse(savedSession) : null;
  });

  const handleAuthenticated = (nextSession) => {
    localStorage.setItem('mental-health-session', JSON.stringify(nextSession));
    setSession(nextSession);
  };

  const handleLogout = () => {
    localStorage.removeItem('mental-health-session');
    setSession(null);
  };

  return (
    <Provider store={store}>
      <Router>
        {!session ? (
          <Routes>
            <Route path="*" element={<Auth onAuthenticated={handleAuthenticated} />} />
          </Routes>
        ) : (
          <div className="app-container">
            <Navbar session={session} onLogout={handleLogout} />
            <div className="app-content">
              <Sidebar />
              <main className="main-content">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/victims" element={<VictimsList />} />
                  <Route path="/victims/:id" element={<VictimDetails />} />
                  <Route path="/alerts" element={<Alerts />} />
                  <Route path="/interventions" element={<Interventions />} />
                  <Route path="/analytics" element={<Analytics />} />
                </Routes>
              </main>
            </div>
          </div>
        )}
      </Router>
    </Provider>
  );
}

export default App;
