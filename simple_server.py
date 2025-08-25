#!/usr/bin/env python3
"""
Simple server script for testing
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../env.local')

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    try:
        print("🚀 Starting Niche Compass Backend Server...")
        print("📊 Environment:", os.getenv('FLASK_ENV', 'development'))
        print("🔧 Debug Mode:", os.getenv('FLASK_DEBUG', 'False'))
        print("🌐 Server will be available at: http://localhost:5000")
        print()
        
        from src.main import create_app
        app = create_app()
        
        print("✅ Flask app created successfully!")
        print("🚀 Starting server...")
        
        # Run the application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("🔍 Check the logs above for more details")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
