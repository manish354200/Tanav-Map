import React, { useState } from 'react';
import { assistantAPI } from '../services/api';

const SupportAssistant = () => {
  const [message, setMessage] = useState('');
  const [reply, setReply] = useState('Hey, I’m here for you. You can share anything, even the little things, and I’ll listen without judging.');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;

    setLoading(true);
    try {
      const response = await assistantAPI.respond(message, 1);
      setReply(response?.data?.reply || 'I’m here with you.');
      setMessage('');
    } catch (error) {
      console.error('Assistant failed:', error);
      setReply('I’m here with you. You can tell me anything, and we can take this one step at a time.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="assistant-panel" style={{
      background: '#fff7fb',
      border: '1px solid #f2d9e8',
      borderRadius: '14px',
      padding: '18px',
      margin: '20px 0',
      boxShadow: '0 8px 18px rgba(0,0,0,0.04)',
    }}>
      <h2 style={{ marginTop: 0, color: '#7c2d6e' }}>Support Assistant</h2>
      <div style={{
        background: '#fdf2f8',
        borderRadius: '12px',
        padding: '14px',
        marginBottom: '12px',
        color: '#4b1d3a',
        lineHeight: 1.5,
      }}>
        {reply}
      </div>

      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Share how you feel..."
        rows={4}
        style={{
          width: '100%',
          padding: '12px',
          borderRadius: '12px',
          border: '1px solid #e9c8dc',
          resize: 'vertical',
          fontSize: '14px',
          boxSizing: 'border-box',
        }}
      />

      <div style={{ marginTop: '10px', display: 'flex', justifyContent: 'flex-end' }}>
        <button
          onClick={handleSend}
          disabled={loading || !message.trim()}
          style={{
            background: '#d946ef',
            color: '#fff',
            border: 'none',
            borderRadius: '10px',
            padding: '10px 18px',
            cursor: loading ? 'wait' : 'pointer',
            fontWeight: 600,
          }}
        >
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default SupportAssistant;
