#!/usr/bin/env python3
"""
Debug script untuk authentication system
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test basic health endpoint"""
    print("🔍 Testing basic health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"✅ Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health Error: {e}")

def test_auth_health():
    """Test authentication health endpoint"""
    print("\n🔍 Testing auth health...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/health")
        print(f"✅ Auth Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Auth Health Error: {e}")

def test_login():
    """Test login endpoint"""
    print("\n🔍 Testing login...")
    try:
        data = {
            "email": "admin@nichecompass.com",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print(f"✅ Login: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print(f"✅ Token received: {token[:50]}...")
            return token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login Error: {e}")
        return None

def test_protected_route(token):
    """Test protected route with token"""
    if not token:
        print("\n❌ No token to test protected route")
        return
    
    print(f"\n🔍 Testing protected route with token...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/keywords/search?q=jewelry", headers=headers)
        print(f"✅ Protected Route: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Response: {response.json()}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Protected Route Error: {e}")

def test_ai_endpoints():
    """Test AI service endpoints"""
    print("\n🔍 Testing AI endpoints...")
    
    # Test AI health
    try:
        response = requests.get(f"{BASE_URL}/api/ai/health")
        print(f"✅ AI Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ AI Health Error: {e}")
    
    # Test AI monitoring
    try:
        response = requests.get(f"{BASE_URL}/api/ai/monitoring/health")
        print(f"✅ AI Monitoring: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ AI Monitoring Error: {e}")

def main():
    print("🚀 Starting Authentication Debug Test...")
    print("=" * 50)
    
    # Test basic endpoints
    test_health()
    test_auth_health()
    test_ai_endpoints()
    
    # Test authentication flow
    token = test_login()
    if token:
        test_protected_route(token)
    
    print("\n" + "=" * 50)
    print("🏁 Debug test completed!")

if __name__ == "__main__":
    main()
