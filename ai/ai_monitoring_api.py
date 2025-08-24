#!/usr/bin/env python3
"""
AI Monitoring API Endpoints for Niche Compass
Provides REST API for monitoring AI services health and performance
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from .ai_monitoring_service import ai_monitor, MonitoringLevel, MetricType
import logging

logger = logging.getLogger(__name__)

# Create Blueprint
ai_monitoring_bp = Blueprint('ai_monitoring', __name__, url_prefix='/api/ai/monitoring')

@ai_monitoring_bp.route('/health', methods=['GET'])
def get_overall_health():
    """Get overall health status of all AI services"""
    try:
        health_summary = ai_monitor.get_overall_health_summary()
        return jsonify({
            'success': True,
            'data': health_summary,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting overall health: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_monitoring_bp.route('/health/<service_name>', methods=['GET'])
def get_service_health(service_name):
    """Get health status of a specific service"""
    try:
        health_check = ai_monitor.get_service_health(service_name)
        if not health_check:
            return jsonify({
                'success': False,
                'error': f'Service {service_name} not found',
                'timestamp': datetime.now().isoformat()
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'service_name': health_check.service_name,
                'status': health_check.status,
                'response_time_ms': health_check.response_time_ms,
                'timestamp': health_check.timestamp.isoformat(),
                'error_message': health_check.error_message,
                'details': health_check.details
            },
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting service health for {service_name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_monitoring_bp.route('/metrics', methods=['GET'])
def get_performance_metrics():
    """Get performance metrics with optional filtering"""
    try:
        # Get query parameters
        service_name = request.args.get('service_name')
        metric_name = request.args.get('metric_name')
        hours = int(request.args.get('hours', 1))
        
        # Validate hours parameter
        if hours < 1 or hours > 168:  # Max 1 week
            return jsonify({
                'success': False,
                'error': 'Hours parameter must be between 1 and 168',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        metrics = ai_monitor.get_performance_metrics(
            service_name=service_name,
            metric_name=metric_name,
            hours=hours
        )
        
        # Convert metrics to serializable format
        metrics_data = []
        for metric in metrics:
            metrics_data.append({
                'service_name': metric.service_name,
                'metric_name': metric.metric_name,
                'metric_type': metric.metric_type.value,
                'value': metric.value,
                'timestamp': metric.timestamp.isoformat(),
                'labels': metric.labels
            })
        
        return jsonify({
            'success': True,
            'data': {
                'metrics': metrics_data,
                'count': len(metrics_data),
                'filters': {
                    'service_name': service_name,
                    'metric_name': metric_name,
                    'hours': hours
                }
            },
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_monitoring_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get alerts with optional filtering"""
    try:
        # Get query parameters
        level = request.args.get('level')
        service_name = request.args.get('service_name')
        acknowledged = request.args.get('acknowledged')
        
        # Parse level parameter
        if level:
            try:
                level = MonitoringLevel(level)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': f'Invalid level: {level}. Valid levels: {[l.value for l in MonitoringLevel]}',
                    'timestamp': datetime.now().isoformat()
                }), 400
        
        # Parse acknowledged parameter
        if acknowledged is not None:
            if acknowledged.lower() in ['true', '1', 'yes']:
                acknowledged = True
            elif acknowledged.lower() in ['false', '0', 'no']:
                acknowledged = False
            else:
                return jsonify({
                    'success': False,
                    'error': 'Invalid acknowledged parameter. Use true/false, 1/0, or yes/no',
                    'timestamp': datetime.now().isoformat()
                }), 400
        
        alerts = ai_monitor.get_alerts(
            level=level,
            service_name=service_name,
            acknowledged=acknowledged
        )
        
        # Convert alerts to serializable format
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                'id': alert.id,
                'service_name': alert.service_name,
                'level': alert.level.value,
                'message': alert.message,
                'timestamp': alert.timestamp.isoformat(),
                'acknowledged': alert.acknowledged,
                'resolved': alert.resolved,
                'metadata': alert.metadata
            })
        
        return jsonify({
            'success': True,
            'data': {
                'alerts': alerts_data,
                'count': len(alerts_data),
                'filters': {
                    'level': level.value if level else None,
                    'service_name': service_name,
                    'acknowledged': acknowledged
                }
            },
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_monitoring_bp.route('/alerts/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    try:
        ai_monitor.acknowledge_alert(alert_id)
        return jsonify({
            'success': True,
            'message': f'Alert {alert_id} acknowledged successfully',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error acknowledging alert {alert_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_monitoring_bp.route('/alerts/<alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve an alert"""
    try:
        ai_monitor.resolve_alert(alert_id)
        return jsonify({
            'success': True,
            'message': f'Alert {alert_id} resolved successfully',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error resolving alert {alert_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_monitoring_bp.route('/dashboard', methods=['GET'])
def get_monitoring_dashboard():
    """Get comprehensive monitoring dashboard data"""
    try:
        # Get all monitoring data
        health_summary = ai_monitor.get_overall_health_summary()
        service_health = ai_monitor.get_service_health()
        recent_metrics = ai_monitor.get_performance_metrics(hours=1)
        active_alerts = ai_monitor.get_alerts(acknowledged=False, resolved=False)
        
        # Calculate metrics summary
        metrics_summary = {}
        for metric in recent_metrics:
            service = metric.service_name
            metric_name = metric.metric_name
            
            if service not in metrics_summary:
                metrics_summary[service] = {}
            
            if metric_name not in metrics_summary[service]:
                metrics_summary[service][metric_name] = {
                    'count': 0,
                    'total_value': 0,
                    'min_value': float('inf'),
                    'max_value': float('-inf')
                }
            
            summary = metrics_summary[service][metric_name]
            summary['count'] += 1
            summary['total_value'] += metric.value
            summary['min_value'] = min(summary['min_value'], metric.value)
            summary['max_value'] = max(summary['max_value'], metric.value)
        
        # Calculate averages
        for service in metrics_summary:
            for metric_name in metrics_summary[service]:
                summary = metrics_summary[service][metric_name]
                if summary['count'] > 0:
                    summary['avg_value'] = summary['total_value'] / summary['count']
                else:
                    summary['avg_value'] = 0
        
        # Convert service health to serializable format
        services_data = {}
        for service_name, health in service_health.items():
            services_data[service_name] = {
                'status': health.status,
                'response_time_ms': health.response_time_ms,
                'last_check': health.timestamp.isoformat(),
                'error_message': health.error_message
            }
        
        return jsonify({
            'success': True,
            'data': {
                'overall_health': health_summary,
                'services': services_data,
                'metrics_summary': metrics_summary,
                'active_alerts_count': len(active_alerts),
                'recent_metrics_count': len(recent_metrics)
            },
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting monitoring dashboard: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_monitoring_bp.route('/config', methods=['GET'])
def get_monitoring_config():
    """Get monitoring service configuration"""
    try:
        config = {
            'monitoring_enabled': ai_monitor.monitoring_enabled,
            'health_check_interval_seconds': ai_monitor.health_check_interval,
            'metrics_retention_hours': ai_monitor.metrics_retention_hours,
            'alert_thresholds': ai_monitor.alert_thresholds
        }
        
        return jsonify({
            'success': True,
            'data': config,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting monitoring config: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@ai_monitoring_bp.route('/config', methods=['PUT'])
def update_monitoring_config():
    """Update monitoring service configuration"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Update configurable parameters
        if 'health_check_interval' in data:
            ai_monitor.health_check_interval = int(data['health_check_interval'])
        
        if 'metrics_retention_hours' in data:
            ai_monitor.metrics_retention_hours = int(data['metrics_retention_hours'])
        
        if 'alert_thresholds' in data:
            for threshold, value in data['alert_thresholds'].items():
                if threshold in ai_monitor.alert_thresholds:
                    ai_monitor.alert_thresholds[threshold] = value
        
        return jsonify({
            'success': True,
            'message': 'Monitoring configuration updated successfully',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error updating monitoring config: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Error handlers
@ai_monitoring_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@ai_monitoring_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500
