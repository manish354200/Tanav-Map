import React, { useState } from 'react';
import { authAPI } from '../services/api';

const Auth = ({ onAuthenticated }) => {
  const [mode, setMode] = useState('login');
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'counselor' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const updateField = (event) => setForm({ ...form, [event.target.name]: event.target.value });

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = mode === 'login'
        ? await authAPI.login(form.email, form.password)
        : await authAPI.signup(form);
      onAuthenticated(response.data);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Unable to complete that request.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-intro">
        <span className="auth-kicker">NIRBHAYA / CARE OPERATIONS</span>
        <h1>Make every signal count.</h1>
        <p>A calmer workspace for teams supporting survivors through recovery.</p>
        <div className="auth-status"><span />Secure case workspace</div>
      </section>
      <section className="auth-panel">
        <div className="auth-heading">
          <span className="auth-mark">N</span>
          <div><strong>Welcome back</strong><span>Access your monitoring workspace</span></div>
        </div>
        <div className="auth-tabs">
          <button className={mode === 'login' ? 'active' : ''} onClick={() => setMode('login')}>Log in</button>
          <button className={mode === 'signup' ? 'active' : ''} onClick={() => setMode('signup')}>Create account</button>
        </div>
        <form onSubmit={submit} className="auth-form">
          {mode === 'signup' && <label>Full name<input name="name" value={form.name} onChange={updateField} placeholder="Your name" required /></label>}
          <label>Work email<input type="email" name="email" value={form.email} onChange={updateField} placeholder="you@organisation.org" required /></label>
          {mode === 'signup' && <label>Role<select name="role" value={form.role} onChange={updateField}><option value="counselor">Counselor</option><option value="officer">Case officer</option><option value="specialist">Mental health specialist</option></select></label>}
          <label>Password<input type="password" name="password" value={form.password} onChange={updateField} placeholder="At least 8 characters" minLength="8" required /></label>
          {error && <p className="auth-error">{error}</p>}
          <button className="auth-submit" disabled={loading}>{loading ? 'Please wait...' : mode === 'login' ? 'Enter workspace' : 'Create workspace'}</button>
        </form>
        <small className="auth-note">By continuing, you agree to protect sensitive case information.</small>
      </section>
    </main>
  );
};

export default Auth;