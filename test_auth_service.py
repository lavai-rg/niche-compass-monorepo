#!/usr/bin/env python3
"""
Test script untuk auth service
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from auth.auth_service import AuthService
from dotenv import load_dotenv

def test_auth_service():
    """Test auth service directly"""
    print("🔍 Testing Auth Service Directly...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv('env.local')
    
    # Create auth service instance
    print("📁 Creating AuthService instance...")
    auth_service = AuthService()
    
    # Check JWT secret
    print(f"\n🔐 JWT Secret Key: {auth_service.secret_key[:30]}...")
    print(f"🔐 JWT Algorithm: {auth_service.algorithm}")
    print(f"🔐 Token Expiry: {auth_service.token_expiry} seconds")
    
    # Test mock user
    print(f"\n👤 Mock Users: {list(auth_service.mock_users.keys())}")
    
    # Test token creation
    print("\n🔑 Testing token creation...")
    user_data = auth_service.mock_users['admin@nichecompass.com']
    token = auth_service.create_access_token(user_data)
    print(f"✅ Token created: {token[:50]}...")
    
    # Test token verification
    print("\n🔍 Testing token verification...")
    payload = auth_service.verify_token(token)
    if payload:
        print(f"✅ Token verified: {payload}")
    else:
        print("❌ Token verification failed")
    
    # Test with wrong secret
    print("\n🧪 Testing with wrong secret...")
    wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbi0wMDEiLCJlbWFpbCI6ImFkbWluQG5pY2hlY29tcGFzcy5jb20iLCJuYW1lIjoiQWRtaW4gVXNlciIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzU2MTcxNzI3LCJpYXQiOjE3NTYwODUzMjd9.APnGkxvET2Nm2_yGPZhotZfyFRe9QkSgTDmm_b37UmA"
    
    # Try to verify with wrong secret
    auth_service.secret_key = "wrong-secret-key"
    wrong_payload = auth_service.verify_token(wrong_token)
    if wrong_payload:
        print(f"❌ Token verified with wrong secret (this should fail): {wrong_payload}")
    else:
        print("✅ Token correctly rejected with wrong secret")
    
    # Restore correct secret
    auth_service.secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    print("\n" + "=" * 50)
    print("🏁 Auth Service test completed!")

if __name__ == "__main__":
    test_auth_service()
