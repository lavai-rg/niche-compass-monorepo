import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AIMonitoringDashboard.css';

const AIMonitoringDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshInterval, setRefreshInterval] = useState(30); // seconds

  useEffect(() => {
    fetchDashboardData();
    
    // Set up auto-refresh
    const interval = setInterval(fetchDashboardData, refreshInterval * 1000);
    
    return () => clearInterval(interval);
  }, [refreshInterval]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/ai/monitoring/dashboard');
      setDashboardData(response.data.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch monitoring data');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return '#10B981'; // green
      case 'degraded':
        return '#F59E0B'; // yellow
      case 'unhealthy':
        return '#EF4444'; // red
      default:
        return '#6B7280'; // gray
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
        return '✅';
      case 'degraded':
        return '⚠️';
      case 'unhealthy':
        return '❌';
      default:
        return '❓';
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatUptime = (percent) => {
    return `${percent.toFixed(1)}%`;
  };

  if (loading && !dashboardData) {
    return (
      <div className="ai-monitoring-dashboard loading">
        <div className="loading-spinner">🔄</div>
        <p>Loading AI Services Monitoring...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="ai-monitoring-dashboard error">
        <div className="error-icon">❌</div>
        <h3>Error Loading Dashboard</h3>
        <p>{error}</p>
        <button onClick={fetchDashboardData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="ai-monitoring-dashboard">
        <p>No monitoring data available</p>
      </div>
    );
  }

  const { overall_health, services, metrics_summary, active_alerts_count } = dashboardData;

  return (
    <div className="ai-monitoring-dashboard">
      <div className="dashboard-header">
        <h2>🤖 AI Services Monitoring Dashboard</h2>
        <div className="dashboard-controls">
          <label>
            Auto-refresh:
            <select 
              value={refreshInterval} 
              onChange={(e) => setRefreshInterval(Number(e.target.value))}
            >
              <option value={10}>10s</option>
              <option value={30}>30s</option>
              <option value={60}>1m</option>
              <option value={300}>5m</option>
            </select>
          </label>
          <button onClick={fetchDashboardData} className="refresh-button">
            🔄 Refresh Now
          </button>
        </div>
      </div>

      {/* Overall Health Summary */}
      <div className="health-summary">
        <h3>🏥 Overall Health Status</h3>
        <div className="health-cards">
          <div className="health-card overall">
            <div className="health-icon" style={{ color: getStatusColor(overall_health.overall_status) }}>
              {getStatusIcon(overall_health.overall_status)}
            </div>
            <div className="health-info">
              <h4>Overall Status</h4>
              <p className="status-text">{overall_health.overall_status.toUpperCase()}</p>
            </div>
          </div>
          
          <div className="health-card">
            <div className="health-icon">📊</div>
            <div className="health-info">
              <h4>Uptime</h4>
              <p>{formatUptime(overall_health.uptime_percent)}</p>
            </div>
          </div>
          
          <div className="health-card">
            <div className="health-icon">🔧</div>
            <div className="health-info">
              <h4>Services</h4>
              <p>{overall_health.services_count}</p>
            </div>
          </div>
          
          <div className="health-card">
            <div className="health-icon">🚨</div>
            <div className="health-info">
              <h4>Active Alerts</h4>
              <p>{active_alerts_count}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Service Status */}
      <div className="service-status">
        <h3>🔍 Individual Service Status</h3>
        <div className="service-grid">
          {Object.entries(services).map(([serviceName, serviceData]) => (
            <div key={serviceName} className="service-card">
              <div className="service-header">
                <h4>{serviceName.replace('_', ' ').toUpperCase()}</h4>
                <span 
                  className="status-badge"
                  style={{ backgroundColor: getStatusColor(serviceData.status) }}
                >
                  {serviceData.status.toUpperCase()}
                </span>
              </div>
              
              <div className="service-details">
                <div className="detail-item">
                  <span className="label">Response Time:</span>
                  <span className="value">{serviceData.response_time_ms.toFixed(2)}ms</span>
                </div>
                
                <div className="detail-item">
                  <span className="label">Last Check:</span>
                  <span className="value">{formatTimestamp(serviceData.last_check)}</span>
                </div>
                
                {serviceData.error_message && (
                  <div className="detail-item error">
                    <span className="label">Error:</span>
                    <span className="value">{serviceData.error_message}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Metrics Summary */}
      <div className="metrics-summary">
        <h3>📈 Performance Metrics (Last Hour)</h3>
        <div className="metrics-grid">
          {Object.entries(metrics_summary).map(([serviceName, serviceMetrics]) => (
            <div key={serviceName} className="service-metrics">
              <h4>{serviceName.replace('_', ' ').toUpperCase()}</h4>
              <div className="metrics-list">
                {Object.entries(serviceMetrics).map(([metricName, metricData]) => (
                  <div key={metricName} className="metric-item">
                    <span className="metric-name">{metricName.replace(/_/g, ' ')}</span>
                    <div className="metric-values">
                      <span className="metric-value">
                        Count: {metricData.count}
                      </span>
                      {metricData.avg_value !== undefined && (
                        <span className="metric-value">
                          Avg: {metricData.avg_value.toFixed(2)}
                        </span>
                      )}
                      {metricData.min_value !== undefined && metricData.max_value !== undefined && (
                        <span className="metric-value">
                          Min: {metricData.min_value.toFixed(2)} | Max: {metricData.max_value.toFixed(2)}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Service Counts */}
      <div className="service-counts">
        <h3>📊 Service Distribution</h3>
        <div className="count-cards">
          <div className="count-card healthy">
            <div className="count-icon">✅</div>
            <div className="count-info">
              <h4>Healthy</h4>
              <p className="count">{overall_health.healthy_count}</p>
            </div>
          </div>
          
          <div className="count-card degraded">
            <div className="count-icon">⚠️</div>
            <div className="count-info">
              <h4>Degraded</h4>
              <p className="count">{overall_health.degraded_count}</p>
            </div>
          </div>
          
          <div className="count-card unhealthy">
            <div className="count-icon">❌</div>
            <div className="count-info">
              <h4>Unhealthy</h4>
              <p className="count">{overall_health.unhealthy_count}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Last Updated */}
      <div className="last-updated">
        <p>Last updated: {formatTimestamp(dashboardData.timestamp || new Date())}</p>
      </div>
    </div>
  );
};

export default AIMonitoringDashboard;
