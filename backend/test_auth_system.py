#!/usr/bin/env python3
"""
Test Authentication System for Niche Compass
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../env.local')

# Test configuration
BASE_URL = "http://localhost:5000"
AUTH_URL = f"{BASE_URL}/api/auth"

def test_auth_health():
    """Test authentication service health"""
    print("🔍 Testing Authentication Service Health...")
    
    try:
        response = requests.get(f"{AUTH_URL}/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("\n🔍 Testing User Registration...")
    
    test_user = {
        "email": "test@nichecompass.com",
        "password": "testpassword123",
        "name": "Test User"
    }
    
    try:
        response = requests.post(
            f"{AUTH_URL}/register",
            json=test_user,
            headers={'Content-Type': 'application/json'}
        )
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_user_login():
    """Test user login"""
    print("\n🔍 Testing User Login...")
    
    # Test with mock user
    login_data = {
        "email": "admin@nichecompass.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{AUTH_URL}/login",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login Successful!")
            print(f"✅ User: {data['user']['name']}")
            print(f"✅ Token: {data['access_token'][:50]}...")
            return data['access_token']
        else:
            print(f"❌ Login Failed: {response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_protected_route(access_token):
    """Test protected route access"""
    print("\n🔍 Testing Protected Route Access...")
    
    if not access_token:
        print("❌ No access token available")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{AUTH_URL}/me", headers=headers)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Protected Route Access Successful!")
            print(f"✅ User Data: {data['user']['name']}")
            return True
        else:
            print(f"❌ Protected Route Access Failed: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_logout():
    """Test user logout"""
    print("\n🔍 Testing User Logout...")
    
    try:
        response = requests.post(f"{AUTH_URL}/logout")
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Niche Compass Authentication System")
    print("=" * 50)
    
    # Test 1: Health Check
    if not test_auth_health():
        print("❌ Authentication service health check failed")
        return
    
    # Test 2: User Registration
    if not test_user_registration():
        print("❌ User registration test failed")
        return
    
    # Test 3: User Login
    access_token = test_user_login()
    if not access_token:
        print("❌ User login test failed")
        return
    
    # Test 4: Protected Route Access
    if not test_protected_route(access_token):
        print("❌ Protected route access test failed")
        return
    
    # Test 5: User Logout
    if not test_logout():
        print("❌ User logout test failed")
        return
    
    print("\n🎉 All Authentication Tests Passed!")
    print("✅ Authentication System is working correctly!")

if __name__ == "__main__":
    main()
