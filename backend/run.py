#!/usr/bin/env python3
"""
Simple script to run the Niche Compass Flask application
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../env.local')

# Add parent directory to path for AI services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    try:
        from src.main import create_app
        
        print("🚀 Starting Niche Compass Backend Server...")
        print("📊 Environment:", os.getenv('FLASK_ENV', 'development'))
        print("🔧 Debug Mode:", os.getenv('FLASK_DEBUG', 'False'))
        print("🌐 Server will be available at: http://localhost:5000")
        print("📋 API Health Check: http://localhost:5000/api/health")
        print("🤖 AI Services: http://localhost:5000/api/ai/*")
        print()
        
        app = create_app()
        
        # Run the application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("🔍 Check the logs above for more details")
        sys.exit(1)
