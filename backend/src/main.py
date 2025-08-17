import os
import sys
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import configuration and database
from src.config import Config
from src.database import db_instance

# Import all route blueprints
from src.routes.user import user_bp
from src.routes.keywords import keywords_bp
from src.routes.niches import niches_bp
from src.routes.products import products_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__, static_folder="/home/ubuntu/niche-compass-frontend/dist")
    
    # Load configuration
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    # Enable CORS for all routes
    CORS(app, origins="*")
    
    # Register blueprints
    logger.info("Registering user_bp blueprint")
    app.register_blueprint(user_bp, url_prefix='/api')
    logger.info("Registering keywords_bp blueprint")
    app.register_blueprint(keywords_bp, url_prefix='/api')
    logger.info("Registering niches_bp blueprint")
    app.register_blueprint(niches_bp, url_prefix='/api')
    logger.info("Registering products_bp blueprint")
    app.register_blueprint(products_bp, url_prefix='/api')
    logger.info("All blueprints registered successfully")
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            db = db_instance.get_database()
            if db is not None:
                db_status = 'connected'
            else:
                db_status = 'disconnected'
        except Exception as e:
            db_status = f'error: {str(e)}'
        
        return {
            'status': 'healthy',
            'database': db_status,
            'version': '1.0.0'
        }
    
    # API info endpoint
    @app.route('/api', methods=['GET'])
    def api_info():
        """API information endpoint"""
        return {
            'name': 'Niche Compass API',
            'version': '1.0.0',
            'description': 'API for Etsy niche research and product analysis',
            'endpoints': {
                'keywords': '/api/keywords/*',
                'niches': '/api/niches/*',
                'products': '/api/products/*',
                'users': '/api/users/*',
                'health': '/api/health'
            }
        }
    
    # Serve frontend files
    @app.route("/")
    def serve_root():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    return app

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    try:
        # Validate configuration
        Config.validate_config()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.warning(f"Configuration validation failed: {e}")
        logger.info("Some features may not work properly without proper configuration")
    
    # Initialize database connection
    try:
        db_instance.connect()
        logger.info("Database connection initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        logger.info("Running in development mode without database")
    
    logger.info("Starting Niche Compass API server...")
    app.run(host='0.0.0.0', port=5000, debug=False)