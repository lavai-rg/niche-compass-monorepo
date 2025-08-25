#!/usr/bin/env python3
"""
Test script untuk Flask app dan authentication
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from main import create_app
from auth.auth_service import AuthService
from dotenv import load_dotenv
import requests
import json

def test_flask_app():
    """Test Flask app dan authentication"""
    print("🔍 Testing Flask App and Authentication...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv('env.local')
    
    # Create Flask app
    print("📁 Creating Flask app...")
    app = create_app()
    
    with app.test_client() as client:
        print("✅ Flask app created successfully")
        
        # Test basic health
        print("\n🔍 Testing basic health...")
        response = client.get('/api/health')
        print(f"✅ Health: {response.status_code} - {response.get_json()}")
        
        # Test auth health
        print("\n🔍 Testing auth health...")
        response = client.get('/api/auth/health')
        print(f"✅ Auth Health: {response.status_code} - {response.get_json()}")
        
        # Test login
        print("\n🔍 Testing login...")
        login_data = {
            "email": "admin@nichecompass.com",
            "password": "password123"
        }
        response = client.post('/api/auth/login', json=login_data)
        print(f"✅ Login: {response.status_code}")
        
        if response.status_code == 200:
            result = response.get_json()
            token = result.get('access_token')
            print(f"✅ Token received: {token[:50]}...")
            
            # Test protected route with token
            print("\n🔍 Testing protected route with token...")
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get('/api/keywords/search?q=jewelry', headers=headers)
            print(f"✅ Protected Route: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ Response: {response.get_json()}")
            else:
                print(f"❌ Error: {response.get_data(as_text=True)}")
        else:
            print(f"❌ Login failed: {response.get_data(as_text=True)}")
    
    print("\n" + "=" * 50)
    print("🏁 Flask app test completed!")

if __name__ == "__main__":
    test_flask_app()
