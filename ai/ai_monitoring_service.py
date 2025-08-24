#!/usr/bin/env python3
"""
AI Service Monitoring System for Niche Compass
Provides comprehensive monitoring, health checks, and performance metrics for AI services
"""
import os
import logging
import json
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import threading
import queue
import requests
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class MonitoringLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

@dataclass
class HealthCheck:
    service_name: str
    status: str  # healthy, degraded, unhealthy
    timestamp: datetime
    response_time_ms: float
    error_message: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceMetric:
    service_name: str
    metric_name: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)

@dataclass
class Alert:
    id: str
    service_name: str
    level: MonitoringLevel
    message: str
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

class AIMonitoringService:
    def __init__(self):
        self.monitoring_enabled = True
        self.health_check_interval = 30  # seconds
        self.metrics_retention_hours = 24
        self.alert_thresholds = {
            'response_time_ms': 1000,  # 1 second
            'error_rate_percent': 5.0,  # 5%
            'rate_limit_remaining': 5,  # 5 requests remaining
            'service_uptime_percent': 95.0  # 95%
        }
        
        # Storage for metrics and health checks
        self.health_checks = deque(maxlen=1000)
        self.performance_metrics = deque(maxlen=10000)
        self.alerts = deque(maxlen=1000)
        self.service_status = {}
        
        # Monitoring thread
        self.monitoring_thread = None
        self.stop_monitoring = False
        
        # Initialize monitoring
        self._start_monitoring()
        
    def _start_monitoring(self):
        """Start background monitoring thread"""
        if self.monitoring_thread is None:
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            logger.info("AI Service Monitoring started")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while not self.stop_monitoring:
            try:
                self._perform_health_checks()
                self._cleanup_old_metrics()
                time.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)  # Wait before retrying
    
    def _perform_health_checks(self):
        """Perform health checks on all AI services"""
        services_to_check = [
            'azure_vision',
            'azure_text_analytics',
            'ai_monitoring'  # Self-monitoring
        ]
        
        for service_name in services_to_check:
            try:
                health_check = self._check_service_health(service_name)
                self.health_checks.append(health_check)
                self.service_status[service_name] = health_check
                
                # Check for alerts
                self._check_alert_conditions(health_check)
                
            except Exception as e:
                logger.error(f"Error checking health for {service_name}: {e}")
                self._create_alert(
                    service_name, 
                    MonitoringLevel.ERROR, 
                    f"Health check failed: {str(e)}"
                )
    
    def _check_service_health(self, service_name: str) -> HealthCheck:
        """Check health of a specific service"""
        start_time = time.time()
        
        try:
            if service_name == 'azure_vision':
                from .azure_vision_service import AzureVisionService
                service = AzureVisionService()
                status_data = service.get_service_status()
                
            elif service_name == 'azure_text_analytics':
                from .azure_text_analytics_service import AzureTextAnalyticsService
                service = AzureTextAnalyticsService()
                status_data = service.get_service_status()
                
            elif service_name == 'ai_monitoring':
                status_data = self._get_self_status()
                
            else:
                raise ValueError(f"Unknown service: {service_name}")
            
            response_time = (time.time() - start_time) * 1000
            
            # Determine overall status
            if status_data.get('status') == 'healthy':
                status = 'healthy'
            elif status_data.get('status') == 'mock_mode':
                status = 'degraded'
            else:
                status = 'unhealthy'
            
            return HealthCheck(
                service_name=service_name,
                status=status,
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details=status_data
            )
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                service_name=service_name,
                status='unhealthy',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                error_message=str(e)
            )
    
    def _get_self_status(self) -> Dict[str, Any]:
        """Get status of the monitoring service itself"""
        return {
            'status': 'healthy',
            'monitoring_enabled': self.monitoring_enabled,
            'health_checks_count': len(self.health_checks),
            'metrics_count': len(self.performance_metrics),
            'alerts_count': len(self.alerts),
            'uptime_percent': self._calculate_uptime_percent(),
            'last_updated': datetime.now().isoformat()
        }
    
    def _calculate_uptime_percent(self) -> float:
        """Calculate overall uptime percentage"""
        if not self.health_checks:
            return 100.0
        
        total_checks = len(self.health_checks)
        healthy_checks = sum(1 for hc in self.health_checks if hc.status == 'healthy')
        
        return (healthy_checks / total_checks) * 100 if total_checks > 0 else 100.0
    
    def _check_alert_conditions(self, health_check: HealthCheck):
        """Check if health check triggers any alerts"""
        # Response time alert
        if health_check.response_time_ms > self.alert_thresholds['response_time_ms']:
            self._create_alert(
                health_check.service_name,
                MonitoringLevel.WARNING,
                f"High response time: {health_check.response_time_ms:.2f}ms"
            )
        
        # Service status alert
        if health_check.status == 'unhealthy':
            self._create_alert(
                health_check.service_name,
                MonitoringLevel.CRITICAL,
                f"Service unhealthy: {health_check.error_message or 'Unknown error'}"
            )
        elif health_check.status == 'degraded':
            self._create_alert(
                health_check.service_name,
                MonitoringLevel.WARNING,
                "Service running in degraded mode"
            )
    
    def _create_alert(self, service_name: str, level: MonitoringLevel, message: str):
        """Create a new alert"""
        alert = Alert(
            id=f"alert_{int(time.time())}_{service_name}",
            service_name=service_name,
            level=level,
            message=message,
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        logger.warning(f"ALERT [{level.value.upper()}] {service_name}: {message}")
    
    def record_metric(self, service_name: str, metric_name: str, 
                     metric_type: MetricType, value: float, 
                     labels: Dict[str, str] = None):
        """Record a performance metric"""
        if not self.monitoring_enabled:
            return
        
        metric = PerformanceMetric(
            service_name=service_name,
            metric_name=metric_name,
            metric_type=metric_type,
            value=value,
            timestamp=datetime.now(),
            labels=labels or {}
        )
        
        self.performance_metrics.append(metric)
    
    def get_service_health(self, service_name: str = None) -> Union[HealthCheck, Dict[str, HealthCheck]]:
        """Get health status of services"""
        if service_name:
            return self.service_status.get(service_name)
        return self.service_status
    
    def get_performance_metrics(self, service_name: str = None, 
                               metric_name: str = None, 
                               hours: int = 1) -> List[PerformanceMetric]:
        """Get performance metrics with optional filtering"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_metrics = [
            m for m in self.performance_metrics
            if m.timestamp >= cutoff_time
        ]
        
        if service_name:
            filtered_metrics = [m for m in filtered_metrics if m.service_name == service_name]
        
        if metric_name:
            filtered_metrics = [m for m in filtered_metrics if m.metric_name == metric_name]
        
        return filtered_metrics
    
    def get_alerts(self, level: MonitoringLevel = None, 
                   service_name: str = None, 
                   acknowledged: bool = None) -> List[Alert]:
        """Get alerts with optional filtering"""
        filtered_alerts = list(self.alerts)
        
        if level:
            filtered_alerts = [a for a in filtered_alerts if a.level == level]
        
        if service_name:
            filtered_alerts = [a for a in filtered_alerts if a.service_name == service_name]
        
        if acknowledged is not None:
            filtered_alerts = [a for a in filtered_alerts if a.acknowledged == acknowledged]
        
        return filtered_alerts
    
    def acknowledge_alert(self, alert_id: str):
        """Mark an alert as acknowledged"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                break
    
    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                break
    
    def get_overall_health_summary(self) -> Dict[str, Any]:
        """Get overall health summary of all services"""
        if not self.service_status:
            return {'overall_status': 'unknown', 'services_count': 0}
        
        services_count = len(self.service_status)
        healthy_count = sum(1 for s in self.service_status.values() if s.status == 'healthy')
        degraded_count = sum(1 for s in self.service_status.values() if s.status == 'degraded')
        unhealthy_count = sum(1 for s in self.service_status.values() if s.status == 'unhealthy')
        
        # Determine overall status
        if unhealthy_count > 0:
            overall_status = 'unhealthy'
        elif degraded_count > 0:
            overall_status = 'degraded'
        else:
            overall_status = 'healthy'
        
        return {
            'overall_status': overall_status,
            'services_count': services_count,
            'healthy_count': healthy_count,
            'degraded_count': degraded_count,
            'unhealthy_count': unhealthy_count,
            'uptime_percent': self._calculate_uptime_percent(),
            'last_updated': datetime.now().isoformat()
        }
    
    def _cleanup_old_metrics(self):
        """Remove old metrics and health checks"""
        cutoff_time = datetime.now() - timedelta(hours=self.metrics_retention_hours)
        
        # Clean up health checks
        while self.health_checks and self.health_checks[0].timestamp < cutoff_time:
            self.health_checks.popleft()
        
        # Clean up performance metrics
        while self.performance_metrics and self.performance_metrics[0].timestamp < cutoff_time:
            self.performance_metrics.popleft()
        
        # Clean up resolved alerts older than 7 days
        alert_cutoff = datetime.now() - timedelta(days=7)
        while self.alerts and self.alerts[0].timestamp < alert_cutoff and self.alerts[0].resolved:
            self.alerts.popleft()
    
    def stop(self):
        """Stop the monitoring service"""
        self.stop_monitoring = True
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("AI Service Monitoring stopped")

# Global monitoring instance
ai_monitor = AIMonitoringService()

# Decorator for automatic metric recording
def monitor_ai_service(service_name: str, metric_name: str, metric_type: MetricType = MetricType.HISTOGRAM):
    """Decorator to automatically record metrics for AI service methods"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # Record success metric
                execution_time = (time.time() - start_time) * 1000
                ai_monitor.record_metric(
                    service_name, 
                    f"{metric_name}_success", 
                    MetricType.COUNTER, 
                    1.0
                )
                ai_monitor.record_metric(
                    service_name, 
                    f"{metric_name}_execution_time", 
                    MetricType.HISTOGRAM, 
                    execution_time
                )
                
                return result
                
            except Exception as e:
                # Record error metric
                ai_monitor.record_metric(
                    service_name, 
                    f"{metric_name}_error", 
                    MetricType.COUNTER, 
                    1.0
                )
                raise e
        
        return wrapper
    return decorator

# Example usage
if __name__ == "__main__":
    # Test monitoring service
    print("AI Monitoring Service Test")
    print("=" * 50)
    
    # Get overall health
    health_summary = ai_monitor.get_overall_health_summary()
    print(f"Overall Health: {health_summary}")
    
    # Wait for some health checks to complete
    time.sleep(35)
    
    # Get service health
    service_health = ai_monitor.get_service_health()
    for service, health in service_health.items():
        print(f"{service}: {health.status} ({health.response_time_ms:.2f}ms)")
    
    # Get alerts
    alerts = ai_monitor.get_alerts()
    print(f"Active Alerts: {len(alerts)}")
    
    # Stop monitoring
    ai_monitor.stop()
