#!/usr/bin/env python3
"""
Production Deployment Script for Niche Compass
This script handles the complete production deployment process
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

try:
    from production_config import is_production_ready, get_missing_configs, get_production_config
except ImportError:
    print("❌ Error: Could not import production configuration")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deployment.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProductionDeployer:
    """Handles production deployment for Niche Compass"""
    
    def __init__(self):
        self.deployment_start_time = time.time()
        self.deployment_steps = []
        self.current_step = 0
        
    def log_step(self, step_name: str, status: str = "STARTED"):
        """Log deployment step"""
        self.current_step += 1
        timestamp = time.strftime("%H:%M:%S")
        message = f"[{timestamp}] Step {self.current_step}: {step_name} - {status}"
        logger.info(message)
        self.deployment_steps.append({
            'step': self.current_step,
            'name': step_name,
            'status': status,
            'timestamp': timestamp
        })
    
    def run_command(self, command: str, description: str) -> bool:
        """Run a shell command and return success status"""
        try:
            logger.info(f"Running: {description}")
            logger.info(f"Command: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                logger.info(f"Output: {result.stdout}")
            
            logger.info(f"✅ {description} completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ {description} failed with exit code {e.returncode}")
            if e.stdout:
                logger.error(f"STDOUT: {e.stdout}")
            if e.stderr:
                logger.error(f"STDERR: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"❌ {description} failed with error: {str(e)}")
            return False
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met for deployment"""
        logger.info("🔍 Checking deployment prerequisites...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            logger.error(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}")
            return False
        
        logger.info(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check required directories
        required_dirs = ['backend', 'frontend', 'ai']
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                logger.error(f"❌ Required directory '{dir_name}' not found")
                return False
            logger.info(f"✅ Directory '{dir_name}' found")
        
        # Check production configuration
        if not is_production_ready():
            missing_configs = get_missing_configs()
            logger.error("❌ Production configuration not ready")
            logger.error(f"Missing critical configs: {missing_configs['critical']}")
            if missing_configs['optional']:
                logger.warning(f"Missing optional configs: {missing_configs['optional']}")
            return False
        
        logger.info("✅ Production configuration is ready")
        return True
    
    def install_dependencies(self) -> bool:
        """Install production dependencies"""
        logger.info("📦 Installing production dependencies...")
        
        # Install backend dependencies
        if not self.run_command(
            "cd backend && pip install -r requirements.txt",
            "Installing backend dependencies"
        ):
            return False
        
        # Install additional production dependencies
        production_deps = [
            "gunicorn",
            "redis",
            "sentry-sdk[flask]",
            "azure-cosmos",
            "azure-storage-blob",
            "azure-applicationinsights"
        ]
        
        for dep in production_deps:
            if not self.run_command(
                f"pip install {dep}",
                f"Installing {dep}"
            ):
                return False
        
        return True
    
    def setup_production_environment(self) -> bool:
        """Setup production environment"""
        logger.info("🏗️ Setting up production environment...")
        
        # Create production directories
        production_dirs = [
            "/var/log/niche-compass",
            "/var/run/niche-compass",
            "/etc/niche-compass"
        ]
        
        for dir_path in production_dirs:
            try:
                os.makedirs(dir_path, exist_ok=True)
                logger.info(f"✅ Created directory: {dir_path}")
            except Exception as e:
                logger.error(f"❌ Failed to create directory {dir_path}: {str(e)}")
                return False
        
        # Setup log rotation
        logrotate_config = """
/var/log/niche-compass/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
"""
        
        try:
            with open("/etc/logrotate.d/niche-compass", "w") as f:
                f.write(logrotate_config)
            logger.info("✅ Log rotation configured")
        except Exception as e:
            logger.warning(f"⚠️ Could not configure log rotation: {str(e)}")
        
        return True
    
    def build_frontend(self) -> bool:
        """Build frontend for production"""
        logger.info("🔨 Building frontend for production...")
        
        # Install frontend dependencies
        if not self.run_command(
            "cd frontend && npm install",
            "Installing frontend dependencies"
        ):
            return False
        
        # Build frontend
        if not self.run_command(
            "cd frontend && npm run build",
            "Building frontend for production"
        ):
            return False
        
        # Copy build to backend static folder
        if not self.run_command(
            "cp -r frontend/dist/* backend/src/static/",
            "Copying frontend build to backend"
        ):
            return False
        
        return True
    
    def setup_database(self) -> bool:
        """Setup production database"""
        logger.info("🗄️ Setting up production database...")
        
        # Import database setup
        try:
            from database_adapter import db_instance
            from production_config import get_production_config
            
            config = get_production_config()
            
            # Test database connection
            if db_instance.connect():
                logger.info("✅ Database connection successful")
                
                # Run database migrations
                if hasattr(db_instance, 'run_migrations'):
                    if db_instance.run_migrations():
                        logger.info("✅ Database migrations completed")
                    else:
                        logger.error("❌ Database migrations failed")
                        return False
                else:
                    logger.warning("⚠️ Database migrations not available")
                
                return True
            else:
                logger.error("❌ Database connection failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Database setup failed: {str(e)}")
            return False
    
    def setup_ai_services(self) -> bool:
        """Setup AI services for production"""
        logger.info("🤖 Setting up AI services for production...")
        
        try:
            from production_config import get_production_config
            config = get_production_config()
            
            # Test AI services
            if config.ai_services_enabled:
                # Test Vision Service
                if config.azure_vision_endpoint and config.azure_vision_api_key:
                    logger.info("✅ Azure Vision service configured")
                else:
                    logger.warning("⚠️ Azure Vision service not configured")
                
                # Test Text Analytics Service
                if config.azure_text_analytics_endpoint and config.azure_text_analytics_api_key:
                    logger.info("✅ Azure Text Analytics service configured")
                else:
                    logger.warning("⚠️ Azure Text Analytics service not configured")
                
                # Test OpenAI Service
                if config.azure_openai_endpoint and config.azure_openai_api_key:
                    logger.info("✅ Azure OpenAI service configured")
                else:
                    logger.warning("⚠️ Azure OpenAI service not configured")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ AI services setup failed: {str(e)}")
            return False
    
    def create_systemd_service(self) -> bool:
        """Create systemd service for production"""
        logger.info("⚙️ Creating systemd service...")
        
        service_content = """[Unit]
Description=Niche Compass Production Service
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/niche-compass-monorepo
Environment=PATH=/path/to/venv/bin
ExecStart=/path/to/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 --access-logfile /var/log/niche-compass/access.log --error-logfile /var/log/niche-compass/error.log backend.src.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        
        try:
            with open("/etc/systemd/system/niche-compass.service", "w") as f:
                f.write(service_content)
            
            # Reload systemd
            if self.run_command("systemctl daemon-reload", "Reloading systemd"):
                logger.info("✅ Systemd service created")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to create systemd service: {str(e)}")
            return False
    
    def start_production_service(self) -> bool:
        """Start production service"""
        logger.info("🚀 Starting production service...")
        
        # Enable and start service
        if not self.run_command(
            "systemctl enable niche-compass",
            "Enabling niche-compass service"
        ):
            return False
        
        if not self.run_command(
            "systemctl start niche-compass",
            "Starting niche-compass service"
        ):
            return False
        
        # Wait for service to start
        time.sleep(5)
        
        # Check service status
        if not self.run_command(
            "systemctl is-active --quiet niche-compass",
            "Checking service status"
        ):
            logger.error("❌ Service failed to start")
            return False
        
        logger.info("✅ Production service started successfully")
        return True
    
    def run_health_checks(self) -> bool:
        """Run production health checks"""
        logger.info("🏥 Running production health checks...")
        
        # Check service status
        if not self.run_command(
            "systemctl status niche-compass --no-pager",
            "Checking service status"
        ):
            return False
        
        # Check if service is listening on port 5000
        if not self.run_command(
            "netstat -tlnp | grep :5000",
            "Checking if service is listening on port 5000"
        ):
            logger.error("❌ Service not listening on port 5000")
            return False
        
        # Test health endpoint
        if not self.run_command(
            "curl -f http://localhost:5000/api/health",
            "Testing health endpoint"
        ):
            logger.error("❌ Health endpoint test failed")
            return False
        
        logger.info("✅ All health checks passed")
        return True
    
    def deploy(self) -> bool:
        """Run complete production deployment"""
        logger.info("🚀 Starting Niche Compass Production Deployment")
        logger.info("=" * 60)
        
        deployment_steps = [
            ("Check Prerequisites", self.check_prerequisites),
            ("Install Dependencies", self.install_dependencies),
            ("Setup Production Environment", self.setup_production_environment),
            ("Build Frontend", self.build_frontend),
            ("Setup Database", self.setup_database),
            ("Setup AI Services", self.setup_ai_services),
            ("Create Systemd Service", self.create_systemd_service),
            ("Start Production Service", self.start_production_service),
            ("Run Health Checks", self.run_health_checks)
        ]
        
        for step_name, step_function in deployment_steps:
            self.log_step(step_name, "STARTED")
            
            if not step_function():
                self.log_step(step_name, "FAILED")
                logger.error(f"❌ Deployment failed at step: {step_name}")
                return False
            
            self.log_step(step_name, "COMPLETED")
        
        # Deployment completed successfully
        deployment_time = time.time() - self.deployment_start_time
        logger.info("=" * 60)
        logger.info(f"🎉 Production Deployment Completed Successfully!")
        logger.info(f"⏱️ Total deployment time: {deployment_time:.2f} seconds")
        logger.info(f"📊 Deployment steps completed: {len(self.deployment_steps)}")
        
        return True
    
    def rollback(self):
        """Rollback deployment if needed"""
        logger.warning("🔄 Rolling back deployment...")
        
        # Stop service
        self.run_command("systemctl stop niche-compass", "Stopping service")
        
        # Disable service
        self.run_command("systemctl disable niche-compass", "Disabling service")
        
        # Remove service file
        self.run_command("rm -f /etc/systemd/system/niche-compass.service", "Removing service file")
        
        # Reload systemd
        self.run_command("systemctl daemon-reload", "Reloading systemd")
        
        logger.warning("🔄 Rollback completed")

def main():
    """Main deployment function"""
    try:
        deployer = ProductionDeployer()
        
        if deployer.deploy():
            logger.info("🎉 Production deployment successful!")
            sys.exit(0)
        else:
            logger.error("❌ Production deployment failed!")
            deployer.rollback()
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.warning("⚠️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error during deployment: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
