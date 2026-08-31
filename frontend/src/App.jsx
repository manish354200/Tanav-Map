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

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="app-container">
          <Navbar />
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
      </Router>
    </Provider>
  );
}

export default App;
