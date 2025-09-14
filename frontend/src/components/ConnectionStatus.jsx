import React, { useState, useEffect } from 'react';
import { healthCheck } from '../api';

export default function ConnectionStatus() {
  const [status, setStatus] = useState('checking');
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        await healthCheck();
        setStatus('connected');
        setError(null);
      } catch (err) {
        setStatus('disconnected');
        setError(err.message);
      }
    };

    checkConnection();
    // Check every 30 seconds
    const interval = setInterval(checkConnection, 30000);
    
    return () => clearInterval(interval);
  }, []);

  if (status === 'checking') {
    return (
      <div className="connection-status checking">
        <span className="status-icon">🔄</span>
        <span>Checking connection...</span>
      </div>
    );
  }

  if (status === 'connected') {
    return (
      <div className="connection-status connected">
        <span className="status-icon">✅</span>
        <span>Backend connected</span>
      </div>
    );
  }

  return (
    <div className="connection-status disconnected">
      <span className="status-icon">❌</span>
      <span>Backend disconnected</span>
      {error && <div className="error-details">{error}</div>}
    </div>
  );
}
