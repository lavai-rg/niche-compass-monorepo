import os
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProductionConfig:
    """Production configuration manager for Niche Compass"""
    
    # Flask Settings
    flask_env: str = "production"
    flask_debug: bool = False
    secret_key: str = ""
    
    # Database Settings
    azure_cosmos_endpoint: str = ""
    azure_cosmos_key: str = ""
    azure_cosmos_database: str = "niche-compass-prod"
    azure_cosmos_container: str = "niche-data"
    
    # AI Services
    azure_vision_endpoint: str = ""
    azure_vision_api_key: str = ""
    azure_text_analytics_endpoint: str = ""
    azure_text_analytics_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment_name: str = ""
    
    # Authentication
    auth0_domain: str = ""
    auth0_audience: str = ""
    auth0_client_id: str = ""
    auth0_client_secret: str = ""
    jwt_secret_key: str = ""
    jwt_access_token_expires: int = 3600
    jwt_refresh_token_expires: int = 604800
    
    # External APIs
    etsy_api_key: str = ""
    etsy_api_secret: str = ""
    etsy_shop_id: str = ""
    twitter_api_key: str = ""
    twitter_api_secret: str = ""
    twitter_access_token: str = ""
    twitter_access_token_secret: str = ""
    
    # Storage
    azure_storage_connection_string: str = ""
    azure_storage_container: str = "niche-compass-files"
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: str = "png,jpg,jpeg,gif,bmp,tiff,webp"
    
    # Monitoring
    azure_app_insights_connection_string: str = ""
    log_level: str = "INFO"
    log_file_path: str = "/var/log/niche-compass/app.log"
    
    # Performance
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    redis_url: str = ""
    cache_type: str = "redis"
    cache_default_timeout: int = 300
    
    # Security
    cors_origins: str = ""
    cors_allow_credentials: bool = True
    strict_transport_security: bool = True
    content_security_policy: str = "default-src 'self'"
    x_frame_options: str = "DENY"
    x_content_type_options: str = "nosniff"
    
    # Error Handling
    sentry_dsn: str = ""
    error_reporting_enabled: bool = True
    
    # Backup
    backup_enabled: bool = True
    backup_schedule: str = "0 2 * * *"
    backup_retention_days: int = 30
    
    # Notifications
    smtp_server: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    slack_webhook_url: str = ""
    
    # Feature Flags
    ai_services_enabled: bool = True
    social_media_integration_enabled: bool = True
    real_time_analytics_enabled: bool = True
    advanced_reporting_enabled: bool = True
    
    # Deployment
    deployment_environment: str = "production"
    deployment_version: str = "1.0.0"
    health_check_endpoint: str = "/api/health"

class ProductionConfigManager:
    """Manages production configuration loading and validation"""
    
    def __init__(self):
        self.config = ProductionConfig()
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables"""
        try:
            # Flask Settings
            self.config.flask_env = os.getenv('FLASK_ENV', 'production')
            self.config.flask_debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
            self.config.secret_key = os.getenv('SECRET_KEY', '')
            
            # Database Settings
            self.config.azure_cosmos_endpoint = os.getenv('AZURE_COSMOS_ENDPOINT', '')
            self.config.azure_cosmos_key = os.getenv('AZURE_COSMOS_KEY', '')
            self.config.azure_cosmos_database = os.getenv('AZURE_COSMOS_DATABASE', 'niche-compass-prod')
            self.config.azure_cosmos_container = os.getenv('AZURE_COSMOS_CONTAINER', 'niche-data')
            
            # AI Services
            self.config.azure_vision_endpoint = os.getenv('AZURE_VISION_ENDPOINT', '')
            self.config.azure_vision_api_key = os.getenv('AZURE_VISION_API_KEY', '')
            self.config.azure_text_analytics_endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT', '')
            self.config.azure_text_analytics_api_key = os.getenv('AZURE_TEXT_ANALYTICS_API_KEY', '')
            self.config.azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '')
            self.config.azure_openai_api_key = os.getenv('AZURE_OPENAI_API_KEY', '')
            self.config.azure_openai_deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', '')
            
            # Authentication
            self.config.auth0_domain = os.getenv('AUTH0_DOMAIN', '')
            self.config.auth0_audience = os.getenv('AUTH0_AUDIENCE', '')
            self.config.auth0_client_id = os.getenv('AUTH0_CLIENT_ID', '')
            self.config.auth0_client_secret = os.getenv('AUTH0_CLIENT_SECRET', '')
            self.config.jwt_secret_key = os.getenv('JWT_SECRET_KEY', '')
            self.config.jwt_access_token_expires = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600'))
            self.config.jwt_refresh_token_expires = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', '604800'))
            
            # External APIs
            self.config.etsy_api_key = os.getenv('ETSY_API_KEY', '')
            self.config.etsy_api_secret = os.getenv('ETSY_API_SECRET', '')
            self.config.etsy_shop_id = os.getenv('ETSY_SHOP_ID', '')
            self.config.twitter_api_key = os.getenv('TWITTER_API_KEY', '')
            self.config.twitter_api_secret = os.getenv('TWITTER_API_SECRET', '')
            self.config.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN', '')
            self.config.twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
            
            # Storage
            self.config.azure_storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING', '')
            self.config.azure_storage_container = os.getenv('AZURE_STORAGE_CONTAINER', 'niche-compass-files')
            self.config.max_file_size = int(os.getenv('MAX_FILE_SIZE', '10485760'))
            self.config.allowed_extensions = os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif,bmp,tiff,webp')
            
            # Monitoring
            self.config.azure_app_insights_connection_string = os.getenv('AZURE_APPLICATION_INSIGHTS_CONNECTION_STRING', '')
            self.config.log_level = os.getenv('LOG_LEVEL', 'INFO')
            self.config.log_file_path = os.getenv('LOG_FILE_PATH', '/var/log/niche-compass/app.log')
            
            # Performance
            self.config.rate_limit_requests = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))
            self.config.rate_limit_window = int(os.getenv('RATE_LIMIT_WINDOW', '60'))
            self.config.redis_url = os.getenv('REDIS_URL', '')
            self.config.cache_type = os.getenv('CACHE_TYPE', 'redis')
            self.config.cache_default_timeout = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
            
            # Security
            self.config.cors_origins = os.getenv('CORS_ORIGINS', '')
            self.config.cors_allow_credentials = os.getenv('CORS_ALLOW_CREDENTIALS', 'True').lower() == 'true'
            self.config.strict_transport_security = os.getenv('STRICT_TRANSPORT_SECURITY', 'True').lower() == 'true'
            self.config.content_security_policy = os.getenv('CONTENT_SECURITY_POLICY', 'default-src \'self\'')
            self.config.x_frame_options = os.getenv('X_FRAME_OPTIONS', 'DENY')
            self.config.x_content_type_options = os.getenv('X_CONTENT_TYPE_OPTIONS', 'nosniff')
            
            # Error Handling
            self.config.sentry_dsn = os.getenv('SENTRY_DSN', '')
            self.config.error_reporting_enabled = os.getenv('ERROR_REPORTING_ENABLED', 'True').lower() == 'true'
            
            # Backup
            self.config.backup_enabled = os.getenv('BACKUP_ENABLED', 'True').lower() == 'true'
            self.config.backup_schedule = os.getenv('BACKUP_SCHEDULE', '0 2 * * *')
            self.config.backup_retention_days = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
            
            # Notifications
            self.config.smtp_server = os.getenv('SMTP_SERVER', '')
            self.config.smtp_port = int(os.getenv('SMTP_PORT', '587'))
            self.config.smtp_username = os.getenv('SMTP_USERNAME', '')
            self.config.smtp_password = os.getenv('SMTP_PASSWORD', '')
            self.config.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL', '')
            
            # Feature Flags
            self.config.ai_services_enabled = os.getenv('AI_SERVICES_ENABLED', 'True').lower() == 'true'
            self.config.social_media_integration_enabled = os.getenv('SOCIAL_MEDIA_INTEGRATION_ENABLED', 'True').lower() == 'true'
            self.config.real_time_analytics_enabled = os.getenv('REAL_TIME_ANALYTICS_ENABLED', 'True').lower() == 'true'
            self.config.advanced_reporting_enabled = os.getenv('ADVANCED_REPORTING_ENABLED', 'True').lower() == 'true'
            
            # Deployment
            self.config.deployment_environment = os.getenv('DEPLOYMENT_ENVIRONMENT', 'production')
            self.config.deployment_version = os.getenv('DEPLOYMENT_VERSION', '1.0.0')
            self.config.health_check_endpoint = os.getenv('HEALTH_CHECK_ENDPOINT', '/api/health')
            
            logger.info("Production configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading production configuration: {str(e)}")
            raise
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate production configuration and return validation results"""
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'missing_critical': [],
            'missing_optional': []
        }
        
        # Critical validations
        critical_fields = [
            'secret_key',
            'azure_cosmos_endpoint',
            'azure_cosmos_key',
            'azure_vision_endpoint',
            'azure_vision_api_key',
            'azure_text_analytics_endpoint',
            'azure_text_analytics_api_key',
            'auth0_domain',
            'auth0_audience',
            'auth0_client_id',
            'auth0_client_secret'
        ]
        
        for field in critical_fields:
            if not getattr(self.config, field):
                validation_results['missing_critical'].append(field)
                validation_results['valid'] = False
        
        # Optional validations
        optional_fields = [
            'azure_openai_endpoint',
            'azure_openai_api_key',
            'etsy_api_key',
            'etsy_api_secret',
            'twitter_api_key',
            'twitter_api_secret',
            'azure_storage_connection_string',
            'redis_url',
            'sentry_dsn'
        ]
        
        for field in optional_fields:
            if not getattr(self.config, field):
                validation_results['missing_optional'].append(field)
        
        # Security validations
        if len(self.config.secret_key) < 32:
            validation_results['warnings'].append('SECRET_KEY should be at least 32 characters long')
        
        if self.config.flask_debug:
            validation_results['warnings'].append('FLASK_DEBUG should be False in production')
        
        # Log validation results
        if validation_results['missing_critical']:
            logger.error(f"Critical configuration missing: {validation_results['missing_critical']}")
        
        if validation_results['missing_optional']:
            logger.warning(f"Optional configuration missing: {validation_results['missing_optional']}")
        
        if validation_results['warnings']:
            for warning in validation_results['warnings']:
                logger.warning(f"Configuration warning: {warning}")
        
        return validation_results
    
    def get_config(self) -> ProductionConfig:
        """Get the production configuration"""
        return self.config
    
    def is_production_ready(self) -> bool:
        """Check if configuration is ready for production"""
        validation = self.validate_config()
        return validation['valid'] and len(validation['missing_critical']) == 0
    
    def get_missing_configs(self) -> Dict[str, list]:
        """Get list of missing configurations"""
        validation = self.validate_config()
        return {
            'critical': validation['missing_critical'],
            'optional': validation['missing_optional']
        }

# Global instance
production_config_manager = ProductionConfigManager()

def get_production_config() -> ProductionConfig:
    """Get production configuration instance"""
    return production_config_manager.get_config()

def is_production_ready() -> bool:
    """Check if production configuration is ready"""
    return production_config_manager.is_production_ready()

def get_missing_configs() -> Dict[str, list]:
    """Get missing configuration details"""
    return production_config_manager.get_missing_configs()
